from typing import Union, Callable
import logging
from pydantic import BaseModel, ValidationError, Field

from fastapi import FastAPI, Security, HTTPException, Request
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import PlainTextResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.status import HTTP_403_FORBIDDEN

from dotenv import load_dotenv
import os

import pinyin_jyutping
import deepl

app_logger = logging.getLogger("myapp_logger")
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
                    )

load_dotenv()
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
p = pinyin_jyutping.PinyinJyutping()

api_keys_env = {k: v for k, v in os.environ.items() if k.startswith('APP_API_KEY_')}
API_KEYS = {value.split(':')[0]: value.split(':')[1] for value in api_keys_env.values()}
API_KEY_NAME = "x-access-token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


class CustomPlainTextResponse(PlainTextResponse):
    media_type = "text/plain; charset=utf-8"

class LargeText(BaseModel):
    text: str = Field(..., description="Hanzi text to translate")

def get_api_key(api_key_header: str = Security(api_key_header)):
    api_key = API_KEYS.get(api_key_header)
    if api_key:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )

@app.get("/", response_class=PlainTextResponse)
@limiter.limit("10/minute")
def read_root(request: Request):
    response = """{}\n{}\n{}""".format("你好世界", "nǐ hǎo shì jiè", "Hello world.")
    return response

@app.get("/pinyin/{hanzi}", response_class=PlainTextResponse)
@limiter.limit("10/minute")
def read_item(hanzi: Union[str, None], request: Request, api_key: str = Security(get_api_key)):

    output_pinyin = p.pinyin(hanzi, spaces=True)

    response = """{}\n{}""".format(hanzi, output_pinyin)
    return response

@app.get("/translate/{hanzi}", response_class=PlainTextResponse)
@limiter.limit("10/minute")
def translate_item(hanzi: Union[str, None], request: Request, api_key: str = Security(get_api_key)):

    translation = translator.translate_text(hanzi, source_lang="ZH", target_lang="EN-GB")
    
    response = """{}\n{}""".format(hanzi, translation)
    return response

@app.get("/pinyin-translate/{hanzi}", response_class=PlainTextResponse)
@limiter.limit("10/minute")
def pinyin_translate_item(hanzi: Union[str, None], request: Request, api_key: str = Security(get_api_key)):

    p = pinyin_jyutping.PinyinJyutping()
    output_pinyin = p.pinyin(hanzi, spaces=True)
    translation = translator.translate_text(hanzi, source_lang="ZH", target_lang="EN-GB")

    response = """{}\n{}\n{}""".format(hanzi, output_pinyin, translation)
    return response

@app.post("/pinyin-translate-bulk", response_class=PlainTextResponse)
@limiter.limit("10/minute")
def pinyin_translate_bulk_item(request: Request, data: LargeText, api_key: str = Security(get_api_key)):

    try:
        text = data.text
        combined_text = text
        #combined_text = text.replace('\n', ' | ')
        
        p = pinyin_jyutping.PinyinJyutping()
        output_pinyin = p.pinyin(combined_text, spaces=True)
        translation = translator.translate_text(combined_text, source_lang="ZH", target_lang="EN-GB")

        # Split the strings into lists of elements
        #split_character = " | "
        split_character = "\n"
        elements1 = combined_text.split(split_character)
        elements2 = output_pinyin.split(split_character)
        elements3 = translation.text.split(split_character)

        for idx, e in enumerate(elements1):
            e = e.strip()
            elements1[idx] = e + ' \n'
        
        for idx, e in enumerate(elements2):
            e = e.strip()
            elements2[idx] = e + ' \n'

        for idx, e in enumerate(elements3):
            e = e.strip()
            elements3[idx] = e + ' \n'

        # Combine the elements from both lists
        combined_elements = [f"{e1} {e2} {e3}" for e1, e2, e3 in zip(elements1, elements2, elements3)]

        # Join the combined elements back into a single string
        result = "\n".join(combined_elements)

        return str(result)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str("Invalid input data. Error: "+e))

@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    api_key = request.headers.get(API_KEY_NAME)
    user_id = API_KEYS.get(api_key, "Unknown")
    app_logger.info(f"Request {request.method} {request.url} by User ID: {user_id}")
    
    response = await call_next(request)
    app_logger.info(f"Response status_code: {response.status_code}")
    return response

if __name__ == "__main__":
    
    p = pinyin_jyutping.PinyinJyutping()
    output_pinyin = p.pinyin("你好")
    print(output_pinyin)
