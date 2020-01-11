from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


key = [["Add task", "Delete task", "Show tasks"]]
markup = ReplyKeyboardMarkup(key)

confirm_keys = [["Yes", "No"]]
confirm_markup = ReplyKeyboardMarkup(confirm_keys)

delete_markup = ReplyKeyboardRemove()
