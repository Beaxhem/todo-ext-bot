import sqlalchemy
import logging

from db import User, Task, Session
from handlers_index import *
from markup import confirm_markup, markup, delete_markup


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    username = update.message["chat"]["username"]
    user = User(username=username)

    session = Session()

    try:
        session.add(user)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        print("User has already been created")

    update.message.reply_text(
        "Hi! I'm the best task manager in Telegram\n"
        "Why don't add your tasks here?",
        reply_markup=markup,
        parse_method="html"
    )

    return CHOOSING


def add(update, context):

    update.message.reply_text("Enter your task", reply_markup=delete_markup)
    return ADD


def add_task(update, context):
    text = update.message.text
    context.user_data["task"] = text

    context.bot.send_message(text="Save?\n"
                             "{}".format(text),
                             chat_id=update.effective_chat.id,
                             reply_markup=confirm_markup)
    return ADD_CONFIRM


def add_confirm(update, context):
    answer = update.message.text

    if answer == "Yes":
        username = update.message["chat"]["username"]
        text = context.user_data["task"]

        session = Session()
        user = session.query(User).filter(User.username == username).one()

        user.tasks.append(Task(text=text))
        session.commit()

        update.message.reply_text("A new task has been successfully created!", reply_markup=markup)
    else:
        del context.user_data["task"]

    return CHOOSING


def delete(update, context):
    update.message.reply_text(
        "Enter the id of the task to delete"
    )

    return DELETE


def delete_id(update, context):
    text = update.message.text
    username = update.message.chat.username

    context.user_data["id"] = text

    session = Session()
    u = session.query(User).filter(User.username == username).one()

    ts = u.tasks

    update.message.reply_text(
        "Are tou sure that you want to delete a task:\n"
        "{}".format(ts[int(text)-1]),
        parse_method="html",
        reply_markup=confirm_markup
    )
    return DELETE_CONFIRM


def delete_confirm(update, context):
    text = update.message.text
    username = update.message.chat.username

    if text == "Yes":
        session = Session()
        u = session.query(User).filter(User.username == username).one()

        ts = u.tasks
        id = int(context.user_data["id"]) - 1

        task = ts[id]

        session.delete(task)
        session.commit()

        del context.user_data["id"]

        update.message.reply_text("You have successfully deleted the task!", reply_markup=markup)
        return CHOOSING
    elif text == "No":
        update.message.reply_text("It's ok", reply_markup=markup)

        return CHOOSING
    else:
        update.message.reply_text("Type 'Yes' or 'No'")

        return DELETE_CONFIRM


def show(update, context):
    username = update.message["chat"]["username"]
    print(username)
    update.message.reply_text(
        "Your tasks:"
        "{}".format(tasks(username))
    )

    return CHOOSING


def tasks(username):
    session = Session()
    r = list()

    u = session.query(User).filter(User.username == username).one()

    for i, t in enumerate(u.tasks):
        r.append("{0}. {1}".format(i+1, t.text))

    return "\n".join(r).join(['\n', '\n'])


def finish(update, context):
    update.message.reply_text("Bye-bye")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
