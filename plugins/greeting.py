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
            
            
      
      
      
      

