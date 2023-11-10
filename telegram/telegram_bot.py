import logging
from bestconfig import Config
from aiogram import Bot, Dispatcher, executor, types

config = Config()

class TelegramBot:
    def __init__(self, api_token):
        self.api_token = api_token
        logging.basicConfig(level=logging.INFO)
        self.bot = Bot(token=self.api_token)
        self.dp = Dispatcher(self.bot)

    async def start(self, message: types.Message):
        print(message)
        await message.answer("Привет! Ответь на три вопроса:\n1. Раз?\n2. Два?\n3. Три?")

    async def process_answers(self, message: types.Message):
        print(message)
        msg = await message.answer("Спасибо за ответы!")
        print('__________')
        print(msg)

    def run(self):
        self.dp.register_message_handler(self.start, commands=['start'])
        self.dp.register_message_handler(self.process_answers)
        executor.start_polling(self.dp, skip_updates=True)
        
tb = TelegramBot(config['API_TOKEN'])
tb.run()