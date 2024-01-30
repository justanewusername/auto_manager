from openai import OpenAI
from bestconfig import Config

class GPTManager:
    def __init__(self) -> None:
        config = Config()
        self.client = OpenAI(api_key=config['GPT_KEY'])
        self.model = config['GPT_MODEL']
        self.prompt = "Сначала сократи статью (не больше 120 слов), чтобы ее можно было использовать для канала в телеграм, а в конце напиши три вопроса для эксперта на основе статьи ниже (представь, что ты берешь интервью и хочешь узнать мнение человека о теме статьи): "
        self.max_tokens = 1500

    def get_post(self, article: str) -> str:
        completion = self.client.completions.create(
            model=self.model,
            prompt= self.prompt + article,
            max_tokens=self.max_tokens,
            temperature=0
        )
        return completion.choices[0].text