from openai import OpenAI
from bestconfig import Config

class GPTManager:
    def __init__(self) -> None:
        config = Config()
        self.client = OpenAI(api_key=config['GPT_KEY'])
        self.model = config['GPT_MODEL']
        self.prompt = "Напиши в стиле, гугл/инстаграм, пост на русском языке максимум 4 абзаца, должен содержать три вопроса для получения мнения от экспертов. Пост составь на основе этой статьи: "
        self.max_tokens = 1500

    def get_post(self, article: str) -> str:
        if len(article) > 4500:
            article = article[0:4500]
        print('**************')
        print('**************')
        print(article)
        print('**************')
        print('**************')
        print('**************')

        completion = self.client.completions.create(
            model=self.model,
            prompt= self.prompt + article,
            max_tokens=self.max_tokens,
            temperature=0
        )
        print(completion)
        return completion.choices[0].text