from typing import Union
from fastapi import FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os

import pinyin_jyutping
import deepl

load_dotenv()
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
p = pinyin_jyutping.PinyinJyutping()

API_KEY = os.getenv("APP_API_KEY")
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

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
def read_root(api_key: str = Security(get_api_key)):
    return {"Hello": "World"}

@app.get("/pinyin/{hanzi}", response_class=PlainTextResponse)
def read_item(hanzi: Union[str, None], api_key: str = Security(get_api_key)):

    output_pinyin = p.pinyin(hanzi, spaces=True)

    response = """{}\n{}""".format(hanzi, output_pinyin)
    return response

@app.get("/translate/{hanzi}", response_class=PlainTextResponse)
def translate_item(hanzi: Union[str, None]):

    translation = translator.translate_text(hanzi, source_lang="ZH", target_lang="EN-GB")
    
    response = """{}\n{}""".format(hanzi, translation)
    return response

@app.get("/pinyin-translate/{hanzi}", response_class=PlainTextResponse)
def pinyin_translate_item(hanzi: Union[str, None]):

    p = pinyin_jyutping.PinyinJyutping()
    output_pinyin = p.pinyin(hanzi, spaces=True)
    translation = translator.translate_text(hanzi, source_lang="ZH", target_lang="EN-GB")

    response = """{}\n{}\n{}""".format(hanzi, output_pinyin, translation)
    return response

if __name__ == "__main__":
    p = pinyin_jyutping.PinyinJyutping()
    output_pinyin = p.pinyin("你好")
    print(output_pinyin)