
import os
import requests, ast, json
from data import config


def create_token():
    params = {'yandexPassportOauthToken': oauth_token}
    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)                                                   
    decode_response = response.content.decode('UTF-8')
    text = json.loads(decode_response) 
    iam_token = text['iamToken']
    return iam_token


oauth_token=config.OAUTH_TOKEN
folder_id = config.FOLDER_ID
os.environ['IAM_TOKEN'] = create_token()


async def detect(text):     
    text = text
    body = {
        
        "text": text,
        "folderId": folder_id,
        "languageCodeHints": ["ru","en"],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(os.environ['IAM_TOKEN'])
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/detect',
        json = body,
        headers = headers
    )
    dict_response = ast.literal_eval(response.text)
    if response.status_code == 401:
        os.environ['IAM_TOKEN'] = create_token()
    elif response.status_code ==200 and dict_response != {}:
        return dict_response['languageCode']
    elif dict_response == {}:
        return 'en'
    

async def mess_user(text):
    target_language = 'ru'              
    texts = text
    detect_language = await detect(text)
    if detect_language == 'ru':
        target_language = 'en'
    elif detect_language == 'en':
        target_language = 'ru'
    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(os.environ['IAM_TOKEN'])
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )
    dict_response = ast.literal_eval(response.text)
    return [dict_response['translations'][0]['text'], detect_language]






