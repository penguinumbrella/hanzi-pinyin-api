# hanzi-pinyin-api
Create a personal REST API to translate Hanzi Chinese characters to Pinyin

## About
This is a simple REST API that translates Hanzi Chinese characters to Pinyin. It uses the following two sources:
- [Pinyin Jyutping Python Library](https://github.com/Language-Tools/pinyin-jyutping)
- [DeepL Translation API](https://www.deepl.com/pro-api?cta=header-pro-api). You need to setup a free account to get the API key

## Installation
1. Clone this repository
2. Install the requirements: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add the following variables, replacing `<your-deepl-api-key>` with your own API key:
```
DEEPL_API_KEY=<your-deepl-api-key>
```
4. Run the app: `python main.py`
5. The app will run by default on `http://127.0.0.1:8000`

## Usage
The API has two endpoints:
- `/` - returns hello world
- `/hanzi/:hanzi-string` - translates a Hanzi string to Pinyin
