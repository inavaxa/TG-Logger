# TG_LOGGER

## Описание (Русский)

**TG_LOGGER** — это скрипт на Python для логирования активности Telegram-аккаунта.  
Он сохраняет входящие и исходящие сообщения, события входа/выхода в сеть и аккаунт, а также действия в чатах в отдельные лог-файлы.

**Возможности:**
- Логгирование сообщений из групп и личных чатов
- Логгирование входа/выхода в сеть и аккаунт
- Логгирование событий чатов (добавление/выход пользователей)
- Сохранение логов в отдельные файлы

---

## Description (English)

**TG_LOGGER** is a Python script for logging Telegram account activity.  
It saves incoming and outgoing messages, login/logout events, and chat actions to separate log files.

**Features:**
- Logging messages from groups and private chats
- Logging online/offline and account login/logout events
- Logging chat actions (user joins/leaves)
- Saving logs to separate files

---

## Инструкция по запуску / How to run

1. **Установите Python 3.7+ / Install Python 3.7+:**  
   [python.org/downloads](https://www.python.org/downloads/)

2. **Установите зависимости / Install dependencies:**  
   ```
   pip install telethon requests
   ```

3. **Настройте параметры / Set up your credentials:**  
   В файле `TG_LOGGER.py` замените:
   ```
   api_id = 'ваш айди'
   api_hash = 'ваш хеш'
   phone = 'ваш номер для входа'
   ```
   на ваши значения из [my.telegram.org](https://my.telegram.org).

4. **Запустите скрипт / Run the script:**  
   ```
   python TG_LOGGER.py
   ```
   При первом запуске потребуется ввести код из Telegram.  
   On first run, you will need to enter the code from Telegram.

5. **Логи сохраняются в файлы / Logs are saved to files:**
   - `account_activity.log`
   - `group_messages.log`
   - `private_messages.log`
   - `status_events.log`
   - `account_events.log`

---

🐰 **Пасхалка / Easter egg:** Этот код написал 1nava. Удачного логгирования!  
🐰 This code was written by 1nava. Happy logging!
