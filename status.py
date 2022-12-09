
def sending(bot, chat_id, **checkstatus):
    message = f'Преподаватель проверил работу {checkstatus["lesson_title"]}, она {"принята." if checkstatus["is_negative"] == "False" else "не принята, исправьте ошибки."} Ссылка на урок: {checkstatus["lesson_url"]}'
    bot.send_message(text=message, chat_id=chat_id)


