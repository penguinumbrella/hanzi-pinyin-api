from typing import Union
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

import pinyin_jyutping

app = FastAPI()

class CustomPlainTextResponse(PlainTextResponse):
    media_type = "text/plain; charset=utf-8"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pinyin/{hanzi}", response_class=PlainTextResponse)
def read_item(hanzi: Union[str, None]):
    p = pinyin_jyutping.PinyinJyutping()
    #output_pinyin = p.pinyin(hanzi, tone_numbers=True, spaces=True)
    output_pinyin = p.pinyin(hanzi, spaces=True)
    print(output_pinyin)
    response = "{}, {}".format(hanzi, output_pinyin)
    return response

if __name__ == "__main__":
    p = pinyin_jyutping.PinyinJyutping()
    output_pinyin = p.pinyin("你好我是英國人")
    print(output_pinyin)