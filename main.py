from typing import Union
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os

import pinyin_jyutping
import deepl

load_dotenv()
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

app = FastAPI()

class CustomPlainTextResponse(PlainTextResponse):
    media_type = "text/plain; charset=utf-8"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pinyin/{hanzi}", response_class=PlainTextResponse)
def read_item(hanzi: Union[str, None]):

    p = pinyin_jyutping.PinyinJyutping()
    output_pinyin = p.pinyin(hanzi, spaces=True)
    translation = translator.translate_text(hanzi, source_lang="ZH", target_lang="EN-GB")

    response = """{}\n{}\n{}""".format(hanzi, output_pinyin, translation)
    return response

if __name__ == "__main__":
    p = pinyin_jyutping.PinyinJyutping()
    output_pinyin = p.pinyin("你好")
    print(output_pinyin)