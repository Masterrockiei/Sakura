import html
from typing import List

from telegram import Bot, Update, ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from tg_bot import dispatcher, LOGGER, DEV_USERS, SUDO_USERS, TIGER_USERS
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.chat_status import (bot_admin, user_admin, is_user_ban_protected, can_restrict,
                                                     is_user_admin, is_user_in_chat, connection_status)
from tg_bot.modules.helper_funcs.extraction import extract_user_and_text
from tg_bot.modules.helper_funcs.string_handling import extract_time
from tg_bot.modules.log_channel import loggable, gloggable


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    
    user_id, reason = extract_user_and_text(message, args)
    
    if not user_id:
        message.reply_text("I doubt that's a user.")
        return log_message
      
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
            
        message.reply_text("Can't seem to find this person.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Oh yeah, ban myself, noob!")
        return log_message 
            
    # dev users to bypass whitelist protection incase of abuse
    if is_user_ban_protected(chat, user_id, member) and user not in DEV_USERS:
        message.reply_text("This user has immunity - I can't ban them.")
        return log_message

     log = (f"<b>{html.escape(chat.title)}:</b>\n"
           f"#BANNED\n"
           f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
           f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}")
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)    
        
     try:
        chat.kick_member(user_id)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(chat.id, "Banned user {}.".format(mention_html(member.user.id, member.user.first_name)),
                        parse_mode=ParseMode.HTML)
        return log
      
      except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('Banned!', quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text("Uhm...that didn't work...")
      
      return log_message
    
    
@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    
    user_id, reason = extract_user_and_text(message, args)
    
    if not user_id:
        message.reply_text("I doubt that's a user.")
        return log_message
      
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User not found":
            raise
            
        message.reply_text("I can't seem to find this user.")
        return log_message
    if user_id == bot.id:
        message.reply_text("I'm not gonna BAN myself, are you crazy?")
        return log_message
      
    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("I don't feel like it.")
        return log_message
      
    if not reason:
        message.reply_text("You haven't specified a time to ban this user for!")
        return log_message

    split_reason = reason.split(None, 1)  
      
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    bantime = extract_time(message, time_val)
      
    if not bantime:
        return log_message
      
      
      
      
      
      
      
      
      
