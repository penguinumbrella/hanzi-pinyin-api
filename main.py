from typing import Union, Callable
import logging

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

API_KEY = os.getenv("APP_API_KEY")
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


class CustomPlainTextResponse(PlainTextResponse):
    media_type = "text/plain; charset=utf-8"

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )

@app.get("/")
@limiter.limit("10/minute")
def read_root(request: Request):
    return {"Hello": "World"}

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

@app.get("/testheaders")
async def test_headers(request: Request):
    return {"headers": dict(request.headers)}

@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    app_logger.info(f"Request {request.method} {request.url}")
    response = await call_next(request)
    app_logger.info(f"Response status_code: {response.status_code}")
    return response

if __name__ == "__main__":
    p = pinyin_jyutping.PinyinJyutping()
    output_pinyin = p.pinyin("你好")
    print(output_pinyin)