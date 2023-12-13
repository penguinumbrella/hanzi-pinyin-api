# hanzi-pinyin-api
Create a personal REST API to translate Hanzi Chinese characters to Pinyin

## About
This is a simple REST API that translates Hanzi Chinese characters to Pinyin. It uses the following two sources:
- [Pinyin Jyutping Python Library](https://github.com/Language-Tools/pinyin-jyutping)
- [DeepL Translation API](https://www.deepl.com/pro-api?cta=header-pro-api). You need to setup a free account to get the API key

## Installation
1. Clone this repository
2. Install the requirements: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add the following variables:
```
APP_API_KEY=<your-api-key>
DEEPL_API_KEY=<your-deepl-api-key>
```
- replace `<your-api-key>` with a secure random string of your choice. This will be used to authenticate requests to the API.
- replace `<your-deepl-api-key>` with your created API key from DeepL.
4. Run the app: `python main.py`
5. The app will run by default on `http://127.0.0.1:8000`

## Usage

When you run the app, you can access the API at `http://127.0.0.1:8000/`. 

You will also need to set the request header `acces_token` to the value of the `APP_API_KEY` variable you set in the `.env` file.

The API has two endpoints:
- `/` - returns hello world
- `/hanzi/:hanzi-string` - translates a Hanzi string to Pinyin
