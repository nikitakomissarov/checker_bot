#  devmanbot #

## Summary
The script is aimed to help Devman students with their routine of checking if their tasks are checked. It's generally based on https://dvmn.org/API, modules are needed you're able to find in requirements.txt.
A

To use the code below you have to:

1. Check requirements.txt and be sure that your virtenv includes each from the needed modules.
2. Retrieve your 'chat_id'. The easiest way is to just write this bot https://t.me/userinfobot.
3. Take your own tokens from Telegram and Devman, then insert they together with 'chat_id' into .env like:

DEVMAN_TOKEN = '****'

TELEGRAM_TOKEN = '****'

CHAT_ID = ****


But DO NOT FORGET to create .env on you local machine first.


## Launch and deploying example from windows prompt:

``` C:\Users\big shot>git clone https://github.com/nikitakomissarov/devmanbot
C:\Users\big shot>cd devmanbot
C:\Users\big shot\devmanbot>python  -m venv env
C:\Users\big shot\devmanbot>env\Scripts\activate.bat
(env) C:\Users\big shot\devmanbot>pip install -r requirements.txt
(env) C:\Users\big shot\devmanbot>python main.py
``` 


P. S.
If you see this traceback:
``` (env) C:\Users\big shot\devmanbot>python main.py
Traceback (most recent call last):
  File "C:\Users\big shot\devmanbot\main.py", line 8, in <module>
    DEVMAN_TOKEN = config['DEVMAN_TOKEN']
KeyError: 'DEVMAN_TOKEN' 
```

That means that you still forgot to create your own .env file for DEVMAN_TOKEN, TELEGRAM_TOKEN and CHAT_ID.


