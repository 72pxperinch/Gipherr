import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from datetime import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Load environment variables from .env
load_dotenv()

# Get the Telegram Bot Token from .env
TOKEN = os.getenv("TELEGRAM_BOT_KEY")

# Dictionary to store project names and their corresponding GIF URLs
projects = {}

def start(update, context):
    print("Received /start command")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Giphy Views Tracker Bot! Send /setproject <project_name> followed by the GIF URL to set up a project.")

def set_project(update, context):
    print("Received /setproject command")
    if len(context.args) < 2:
        update.message.reply_text("Please provide both a project name and the GIF URL.")
        return
    project_name = context.args[0]
    gif_url = context.args[1]
    chat_id = update.message.chat_id
    if chat_id not in projects:
        projects[chat_id] = []
    projects[chat_id].append((project_name, gif_url))
    print(f"Project '{project_name}' set successfully with GIF URL: {gif_url}")
    update.message.reply_text(f"Project '{project_name}' set successfully with GIF URL: {gif_url}")

def list_projects(update, context):
    chat_id = update.message.chat_id
    if chat_id in projects:
        project_list = "\n".join([f"{i+1}. {project[0]}" for i, project in enumerate(projects[chat_id])])
        update.message.reply_text(f"List of projects:\n{project_list}")
    else:
        update.message.reply_text("No projects set yet.")

def get_views(update, context):
    chat_id = update.message.chat_id
    if chat_id not in projects:
        update.message.reply_text("No projects set. Use /setproject <project_name> followed by the <GIF_URL> to set up a project.")
        return

    for project_name, gif_url in projects[chat_id]:
        views = fetch_views(gif_url)
        update.message.reply_text(f"Total views for {project_name}: {views}")



def fetch_views(gif_url):
    print(f"Fetching views for GIF URL: {gif_url}")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(gif_url)
    try:
        view_div = driver.find_element(By.CLASS_NAME,"ViewCountContainer-sc-15ri43l")
        if view_div:
            views_text = view_div.text
            driver.quit()
            return views_text
    except NoSuchElementException:
        driver.quit()
        return "Views not found"
    return "Views not found"

def remove_project(update, context):
    chat_id = update.message.chat_id
    if chat_id not in projects:
        update.message.reply_text("No projects set yet.")
        return

    args = context.args
    if len(args) == 0:
        update.message.reply_text("Please specify the name of the project you want to remove.")
        return

    project_name = " ".join(args)
    removed = False
    for project in projects[chat_id]:
        if project_name.lower() in project[0].lower():
            projects[chat_id].remove(project)
            removed = True
            update.message.reply_text(f"Project '{project_name}' removed successfully.")
            break

    if not removed:
        update.message.reply_text(f"Project '{project_name}' not found.")


def daily_update(context):
    print("Running daily update")
    for chat_id, project_list in projects.items():
        for project_name, gif_url in project_list:
            views = fetch_views(gif_url)
            print(f"Daily update for {project_name}: {views} views")
            context.bot.send_message(chat_id=chat_id, text=f"Daily update for {project_name}: {views}")

def main():
    updater = Updater(TOKEN, use_context=True)
    print("Bot Initiated")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setproject", set_project))
    dp.add_handler(CommandHandler("listprojects", list_projects))
    dp.add_handler(CommandHandler("getviews", get_views))
    dp.add_handler(CommandHandler("removeproject", remove_project))


    updater.start_polling()

    # Schedule daily updates
    job_queue = updater.job_queue
    job_queue.run_daily(daily_update, time=time(hour=8, minute=0, second=0))
    job_queue.run_daily(daily_update, time=time(hour=20, minute=0, second=0))


    updater.idle()

if __name__ == '__main__':
    main()
