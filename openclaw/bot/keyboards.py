"""Inline keyboard helpers."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Yes", callback_data="confirm:yes"),
            InlineKeyboardButton("No", callback_data="confirm:no"),
        ]]
    )
