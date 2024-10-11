import requests


class YandexGPT:
    def __init__(self, token, catalog):
        self.token = token
        self.catalog = catalog

    def send_request(self, question):
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        prompt = {
            "modelUri": f'gpt://{self.catalog}/yandexgpt-lite',
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 200
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Отвечай цитатами из книг"
                },
                {
                    "role": "user",
                    "text": f"{question}"
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.token}"
        }

        response = requests.post(url, headers=headers, json=prompt)
        text = response.json()['result']['alternatives'][0]['message']['text']
        return text


token = ''
catalog = ''

bot = YandexGPT(token, catalog)
res = bot.send_request("Что такое любовь?")
print(res)
