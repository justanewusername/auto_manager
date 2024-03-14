from aiogram import Bot, Dispatcher, executor, types

class TelegramBot:
    def __init__(self, api_token):
        self.api_token = api_token
        self.bot = Bot(token=self.api_token)
        self.dp = Dispatcher(self.bot)

    async def start(self, message: types.Message):
        # print(message)
        await message.answer("""Researchers have developed a new reinforcement learning approach that uses crowdsourced feedback to teach an AI agent how to perform a task without the need for an expertly designed reward function. This method allows for faster learning and can be scaled up for complex tasks. The agent is guided by nonexpert users, who provide feedback on its actions, allowing it to explore and learn more quickly. This approach has been successfully tested on simulated and real-world tasks, and the researchers are working on further improvements and applications.

1. What are the main challenges in teaching an AI agent a new task using reinforcement learning?
2. How does the new approach, HuGE, differ from previous methods that also use nonexpert feedback?
3. What are the potential applications of this method in the future, and how do you ensure that AI agents are aligned with human values?""")

    async def process_answers(self, message: types.Message):
        print(type(message))
        if 'reply_to_message' in message:
            if 'text' in message['reply_to_message']:
                print(message['reply_to_message']['text'])
                await message.answer("Спасибо за ответ!")
        else:
            await message.answer("Вы должны написать ответ к одному из сообщений")

    def run(self):
        self.dp.register_message_handler(self.start, commands=['start'])
        self.dp.register_message_handler(self.process_answers)
        executor.start_polling(self.dp, skip_updates=True)

t = TelegramBot('6833132952:AAEGU-cqcCUPThlDpqRmm4oP-9f5a6P5U_U')
t.run()