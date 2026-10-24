# app/bot/keyboards/main_menu.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.emoji_map import E

def main_menu_kb() -> InlineKeyboardMarkup:
    E_ = E
    kb = [
        [InlineKeyboardButton(f"{E_['browse']} BROWSE", callback_data="browse"),
         InlineKeyboardButton(f"{E_['library']} MY LIBRARY", callback_data="library")],

        [InlineKeyboardButton(f"{E_['age']} BY AGE", callback_data="browse:age"),
         InlineKeyboardButton(f"{E_['studio']} BY STUDIO", callback_data="browse:studio"),
         InlineKeyboardButton(f"{E_['era']} BY ERA", callback_data="browse:era")],

        [InlineKeyboardButton("7–9", callback_data="age:7-9"),
         InlineKeyboardButton("10–12", callback_data="age:10-12"),
         InlineKeyboardButton("13–14", callback_data="age:13-14"),
         InlineKeyboardButton("15–17", callback_data="age:15-17")],

        [InlineKeyboardButton(f"{E_['ethnicity']} ETHNICITY", callback_data="browse:ethnicity"),
         InlineKeyboardButton(f"{E_['featured']} FEATURED", callback_data="featured"),
         InlineKeyboardButton(f"{E_['full_sets']} FULL SETS", callback_data="full_sets")],

        [InlineKeyboardButton(f"{E_['new']} NEW", callback_data="new"),
         InlineKeyboardButton(f"{E_['top']} TOP", callback_data="top"),
         InlineKeyboardButton(f"{E_['rare']} RARE", callback_data="rare")],

        [InlineKeyboardButton(f"{E_['search']} SEARCH", callback_data="search"),
         InlineKeyboardButton(f"{E_['tags']} TAGS", callback_data="tags"),
         InlineKeyboardButton(f"{E_['quality']} QUALITY", callback_data="quality")],

        [InlineKeyboardButton(f"{E_['purchases']} PURCHASES", callback_data="purchases"),
         InlineKeyboardButton(f"{E_['credits']} CREDITS", callback_data="credits"),
         InlineKeyboardButton(f"{E_['codes']} CODES", callback_data="codes")],

        [InlineKeyboardButton(f"{E_['sources']} SOURCES", callback_data="sources"),
         InlineKeyboardButton(f"{E_['trust']} TRUST", callback_data="trust"),
         InlineKeyboardButton(f"{E_['how']} HOW IT WORKS", callback_data="how")],

        [InlineKeyboardButton(f"{E_['channel']} CHANNEL", url="https://t.me/your_channel"),
         InlineKeyboardButton(f"{E_['refer']} REFER & EARN", callback_data="refer"),
         InlineKeyboardButton(f"{E_['admin']} ADMIN", callback_data="admin")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


main_menu = main_menu_kb