# -----------------------------------------------------------------------------
# TG_LOGGER.py
# (c) 2024 1nava
# Все права защищены.
#
# Данный файл является частью проекта для логгирования активности Telegram.
# Использование, копирование и распространение данного кода разрешается только с указанием авторства.
#
# Пасхалка: Этот код написан 1nava. Удачного логгирования! :)
# -----------------------------------------------------------------------------

import logging
from telethon import TelegramClient, events
import asyncio
from telethon.tl.types import (UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, UserStatusLastWeek)
from telethon import functions

# Настройка логгирования
logging.basicConfig(filename='account_activity.log', level=logging.INFO, format='%(asctime)s - %(message)s')

api_id = 'ваш айди'
api_hash = 'ваш хеш'
phone = 'ваш номер для входа'

client = TelegramClient('anon', api_id, api_hash)

# Логгирование сообщений из групп в отдельный файл
group_logger = logging.getLogger('group_logger')
group_handler = logging.FileHandler('group_messages.log', encoding='utf-8')
group_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
group_logger.addHandler(group_handler)
group_logger.setLevel(logging.INFO)

# Логгирование сообщений из личных чатов в отдельный файл
private_logger = logging.getLogger('private_logger')
private_handler = logging.FileHandler('private_messages.log', encoding='utf-8')
private_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
private_logger.addHandler(private_handler)
private_logger.setLevel(logging.INFO)

# Логгирование входа/выхода из сети в отдельный файл
status_logger = logging.getLogger('status_logger')
status_handler = logging.FileHandler('status_events.log', encoding='utf-8')
status_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
status_logger.addHandler(status_handler)
status_logger.setLevel(logging.INFO)

# Логгирование входа/выхода из аккаунта в отдельный файл
account_logger = logging.getLogger('account_logger')
account_handler = logging.FileHandler('account_events.log', encoding='utf-8')
account_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
account_logger.addHandler(account_handler)
account_logger.setLevel(logging.INFO)

# Входящие сообщения
def log_event(event_type, details):
    logging.info(f'{event_type}: {details}')

@client.on(events.NewMessage(incoming=True))
async def log_incoming(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    sender_name = sender.username if sender and sender.username else f'User {event.sender_id}'
    if hasattr(chat, 'title'):
        chat_type = 'Группа'
        chat_name = chat.title
        group_logger.info(f'Входящее сообщение в группе "{chat_name}" от {sender_name}: {event.text}')
    else:
        chat_type = 'Личное'
        chat_name = sender_name
        private_logger.info(f'Входящее личное сообщение от {sender_name}: {event.text}')
    log_event(f'Входящее сообщение ({chat_type})', f'от {sender_name} в "{chat_name}": {event.text}')

@client.on(events.NewMessage(outgoing=True))
async def log_outgoing(event):
    chat = await event.get_chat()
    recipient = None
    if hasattr(chat, 'title'):
        chat_type = 'Группа'
        chat_name = chat.title
        group_logger.info(f'Исходящее сообщение в группе "{chat_name}": {event.text}')
        recipient = chat_name
    else:
        chat_type = 'Личное'
        # Для исходящих сообщений получатель — это chat (User)
        if hasattr(chat, 'username') and chat.username:
            recipient = chat.username
        elif hasattr(chat, 'first_name') and chat.first_name:
            recipient = chat.first_name
        else:
            recipient = f'User {event.chat_id}'
        chat_name = recipient
        private_logger.info(f'Исходящее личное сообщение для {recipient}: {event.text}')
    log_event(f'Исходящее сообщение ({chat_type})', f'для {recipient}: {event.text}')

@client.on(events.ChatAction())
async def handler(event):
    if event.user_joined or event.user_added:
        log_event('Добавление в чат', f'Пользователь {event.user_id} присоединился к чату {event.chat_id}')
    elif event.user_left or event.user_kicked:
        log_event('Покинул чат', f'Пользователь {event.user_id} покинул чат {event.chat_id}')

@client.on(events.Raw())
async def raw_handler(event):
    log_event('Raw event', str(event))

@client.on(events.UserUpdate())
async def user_update_handler(event):
    if hasattr(event, 'status'):
        status = event.status
        user_id = event.user_id
        # Получаем id своего аккаунта
        me = await client.get_me()
        if user_id != me.id:
            return  # Логгируем только свой аккаунт
        try:
            user = await client.get_entity(user_id)
            username = user.username if hasattr(user, 'username') and user.username else f'User {user_id}'
        except Exception:
            username = f'User {user_id}'
        if isinstance(status, UserStatusOnline):
            from datetime import datetime
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                sessions = await client(functions.account.GetAuthorizationsRequest())
                session_info = None
                is_bot = False
                for s in sessions.authorizations:
                    if s.current:
                        device = s.device_model or 'Unknown device'
                        platform = s.platform or 'Unknown platform'
                        app = s.app_name or 'Unknown app'
                        ip = s.ip or 'Unknown IP'
                        session_info = f'{device}, {platform}, {app}, IP: {ip}'
                        if 'bot' in app.lower():
                            is_bot = True
                        break
                bot_status = ' (бот)' if is_bot else ''
                if session_info:
                    status_logger.info(f'Вход в сеть: {username} в {now} с устройства: {session_info}{bot_status}')
                    log_event('Вход в сеть', f'{username} в {now} с устройства: {session_info}{bot_status}')
                else:
                    status_logger.info(f'Вход в сеть: {username} в {now}{bot_status}')
                    log_event('Вход в сеть', f'{username} в {now}{bot_status}')
            except Exception as e:
                status_logger.info(f'Вход в сеть: {username} в {now} (ошибка получения устройства: {e})')
                log_event('Вход в сеть', f'{username} в {now} (ошибка получения устройства: {e})')
        elif isinstance(status, UserStatusOffline):
            status_logger.info(f'Выход из сети: {username}. Был в сети: {status.was_online}')
            log_event('Выход из сети', f'{username}. Был в сети: {status.was_online}')

async def log_own_status():
    while True:
        me = await client.get_me()
        if hasattr(me, 'status'):
            status = me.status
            if isinstance(status, UserStatusOnline):
                log_event('Статус', 'В сети')
            elif isinstance(status, UserStatusOffline):
                log_event('Статус', f'Был в сети: {status.was_online}')
            elif isinstance(status, UserStatusRecently):
                log_event('Статус', 'Был в сети недавно')
            elif isinstance(status, UserStatusLastWeek):
                log_event('Статус', 'Был в сети на прошлой неделе')
            elif isinstance(status, UserStatusLastMonth):
                log_event('Статус', 'Был в сети в прошлом месяце')
            else:
                log_event('Статус', str(status))
        await asyncio.sleep(60)  # Проверять каждую минуту

async def main():
    print("🐰 Пасхалка: Этот код написал 1nava. Удачного логгирования!")
    await client.start(phone=phone)
    me = await client.get_me()
    username = me.username if me and me.username else f'User {me.id}'
    account_logger.info(f'Вход в аккаунт: {username}')
    log_event('Вход в аккаунт', f'{username}')
    print('Логгирование запущено. Для остановки нажмите Ctrl+C')
    try:
        await asyncio.gather(
            log_own_status(),
            client.run_until_disconnected()
        )
    finally:
        account_logger.info('Выход из аккаунта')
        log_event('Выход из аккаунта', 'Текущий аккаунт')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
