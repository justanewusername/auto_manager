from aiogram import Bot, Dispatcher, types, executor
from bestconfig import Config
from database_manager import DatabaseManager

class TelegramSender:
    def __init__(self) -> None:
        self.config = Config()
        API_TOKEN = str(self.config['API_TOKEN'])
        self.bot = Bot(token=API_TOKEN)
        self.dp = Dispatcher(self.bot)

    async def send_message(self, post):
        if len(post) > 4000:
            post = post[0:4000]
        db = DatabaseManager(self.config['DB_CONNECTION'])
        all_users = db.get_all_telegram_users()
        print(f'was found {len(all_users)} users')
        messages_list = []

        for user in all_users:
            try:
                print('wow!')
                message = await self.bot.send_message(user, post)
                message_id = message.message_id
                messages_list.append(message_id)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        return messages_list