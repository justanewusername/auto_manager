from openai import OpenAI
from bestconfig import Config

class GPTManager:
    def __init__(self) -> None:
        config = Config()
        self.client = OpenAI(api_key=config['GPT_KEY'])
        self.model = config['GPT_MODEL']
        self.prompt = "Напиши в стиле, допустим, гугл/инстаграм, пост (на русском языке) максимум 4 абзаца, должен содержать описание, финальный вопрос, на который читатели могут оставить комментарий. Пост составь на основе этой статьи: "
        self.max_tokens = 1500

    def get_post(self, article: str) -> str:
        completion = self.client.completions.create(
            model=self.model,
            prompt= self.prompt + article,
            max_tokens=self.max_tokens,
            temperature=0
        )
        return completion.choices[0].text