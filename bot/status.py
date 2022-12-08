

class Status:
    def __init__(self, chat_id, bot, **checkstatus):
        self.chat_id = chat_id
        self.checkstatus = checkstatus
        self.bot = bot

    def sending(self):
        if self.checkstatus['status'] == 'found' and self.checkstatus['is_negative'] == 'False':
            self.bot.send_message(text=f'Преподаватель проверил работу {self.checkstatus["lesson_title"]}! Она принята. Ссылка на урок: {self.checkstatus["lesson_url"]}', chat_id=self.chat_id)
        else:
            self.bot.send_message(text=f'Преподаватель проверил работу {self.checkstatus["lesson_title"]}!  Но она не принята, исправьте ошибки. Ссылка на урок: {self.checkstatus["lesson_url"]}', chat_id=self.chat_id)