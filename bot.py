import logging
import re
import paramiko
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import Error
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

load_dotenv()

TOKEN = os.getenv('TOKEN')

host = os.getenv("RM_HOST")
host_username = os.getenv("RM_USER")
host_password = os.getenv("RM_PASSWORD")
host_port = os.getenv("RM_PORT")

db = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")

db_vers = os.getenv("P_VERS_M")

gl_email_list = []
gl_number_list = []

def db_connect():
    connection = None
    try:
        connection = psycopg2.connect(user=db_user,
                                      password=db_password,
                                      host=db,
                                      port=db_port,
                                      database=db_database)
    except (Exception, Error):
        pass
    finally:
        return connection

def ssh_conn():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=host_username, password=host_password, port=int(host_port))
    return client

logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

def get_release(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('lsb_release -a')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_uname(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()
def get_uptime(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_df(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_free(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_mpstat(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_w(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_auths(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('tail /var/log/auth.log')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_critical(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('tail /var/log/syslog -n5')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_ps(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('ps | head')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_ss(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('ss -tunlp')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_services(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command('systemctl list-units --type=service --state=running | head') #  output to big
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_repl_logs(update: Update, context):
    client = ssh_conn()
    stdin, stdout, stderr = client.exec_command(f'cat /var/log/postgresql/postgresql-{db_vers}-main.log | grep -a repl | tail')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()

def get_emails(update: Update, context):
    connection = db_connect()
    if connection != None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emails;")
        data = cursor.fetchall()
        emails = ""
        for i in data:
            emails += f'{str(i[0])}. {i[1]}\n'
        update.message.reply_text(emails)
        connection.close()
    else:
        update.message.reply_text("Не удалось подключиться")

def get_numbers(update: Update, context):
    connection = db_connect()
    if connection != None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM numbers;")
        data = cursor.fetchall()
        numbers = ""
        for i in data:
            numbers += f'{str(i[0])}. {i[1]}\n'
        update.message.reply_text(numbers)
        connection.close()
    else:
        update.message.reply_text("Не удалось подключиться")

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'


def findPhoneNumbers(update: Update, context):
    global gl_number_list
    user_input = update.message.text

    phoneNumRegex = re.compile(r'(8|\+7)(\d{10}|\(\d{3}\)\d{7}| \d{3} \d{3} \d{2} \d{2}| \(\d{3}\) \d{3} \d{2} \d{2}|-\d{3}-\d{3}-\d{2}-\d{2})')

    phoneNumberList = phoneNumRegex.findall(user_input)

    if not phoneNumberList:
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END

    phoneNumbers = ''
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {"".join(phoneNumberList[i])}\n'
    phoneNumbers += "Напишите ДА, чтобы записать номера в базу данных или НЕТ, чтобы закончить.\n"
    update.message.reply_text(phoneNumbers)
    gl_number_list = phoneNumberList
    return "number_continue"

def number_continue(update: Update, context):
    user_input = update.message.text
    global gl_number_list
    if user_input == "ДА":
        connection = db_connect()
        if connection != None:
            cursor = connection.cursor()
            for i in gl_number_list:
                cursor.execute(f"INSERT INTO numbers (NUMBER) VALUES ('{''.join(i)}');")
                connection.commit()
            update.message.reply_text("Номера внесены в базу, можете проверить командой /get_numbers.")

        else:
            update.message.reply_text("Не удалось подключиться")
        connection.close()
    gl_number_list = []
    return ConversationHandler.END

def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email-адресов: ')

    return 'findEmail'

def findEmail(update: Update, context):
    global gl_email_list
    user_input = update.message.text

    emailRegex = re.compile(r'\w+@\w+.\w+')

    emailList = emailRegex.findall(user_input)

    if not emailList:
        update.message.reply_text('Email-адреса не найдены')
        return ConversationHandler.END

    emails = ''
    for i in range(len(emailList)):
        emails += f'{i + 1}. {emailList[i]}\n'
    emails += "Напишите ДА, чтобы записать адреса в базу данных или НЕТ, чтобы закончить.\n"
    update.message.reply_text(emails)
    gl_email_list = emailList
    return "email_continue"

def email_continue(update: Update, context):
    user_input = update.message.text
    global gl_email_list
    if user_input == "ДА":
        connection = db_connect()
        if connection != None:
            cursor = connection.cursor()
            for i in gl_email_list:
                cursor.execute(f"INSERT INTO emails (EMAIL) VALUES ('{i}');")
                connection.commit()
            update.message.reply_text("Email адреса внесены в базу, можете проверить командой /get_emails.")

        else:
            update.message.reply_text("Не удалось подключиться")
        connection.close()
    else:
        gl_email_list = []
    return ConversationHandler.END

def checkPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль, который нужно проверить: ')

    return 'checkPassword'

def checkPassword(update: Update, context):
    user_input = update.message.text
    checks = [len(user_input) >= 8,
              re.compile(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]').findall(user_input) != [],
              re.compile(r'[abcdefghijklmnopqrstuvwxyz]').findall(user_input) != [],
              re.compile(r'\d').findall(user_input) != [],
              re.compile(r'[!@#$%^&*()]').findall(user_input) != []]

    if not all(checks):
        update.message.reply_text('Пароль простой')
        return
    update.message.reply_text('Пароль сложный')
    return ConversationHandler.END

def get_apt_listCommand(update: Update, context):
    update.message.reply_text('Введите нужный пакет или "ВСЕ": ')

    return 'get_apt_list'

def get_apt_list(update: Update, context):
    user_input = update.message.text
    client = ssh_conn()
    if user_input == "ВСЕ":
        stdin, stdout, stderr = client.exec_command('apt list --installed | head') # output to big
    else:
        stdin, stdout, stderr = client.exec_command(f'apt show {user_input}')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    client.close()
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    convHandlerCommands = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand), CommandHandler('find_email', findEmailCommand),
                      CommandHandler('verify_password', checkPasswordCommand), CommandHandler('get_apt_list', get_apt_listCommand) ],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, findEmail)],
            'checkPassword': [MessageHandler(Filters.text & ~Filters.command, checkPassword)],
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
            'email_continue': [MessageHandler(Filters.text & ~Filters.command, email_continue)],
            'number_continue': [MessageHandler(Filters.text & ~Filters.command, number_continue)]
        },
        fallbacks=[]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get_release", get_release))
    dp.add_handler(CommandHandler("get_uname", get_uname))
    dp.add_handler(CommandHandler("get_uptime", get_uptime))
    dp.add_handler(CommandHandler("get_df", get_df))
    dp.add_handler(CommandHandler("get_free", get_free))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
    dp.add_handler(CommandHandler("get_w", get_w))
    dp.add_handler(CommandHandler("get_auths", get_auths))
    dp.add_handler(CommandHandler("get_critical", get_critical))
    dp.add_handler(CommandHandler("get_ps", get_ps))
    dp.add_handler(CommandHandler("get_ss", get_ss))
    dp.add_handler(CommandHandler("get_services", get_services))
    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))
    dp.add_handler(CommandHandler("get_emails", get_emails))
    dp.add_handler(CommandHandler("get_numbers", get_numbers))
    dp.add_handler(convHandlerCommands)


    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
