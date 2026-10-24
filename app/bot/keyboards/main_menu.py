# app/bot/keyboards/main_menu.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.emoji_map import E

def main_menu_kb() -> InlineKeyboardMarkup:
    E_ = E
    kb = [
        [InlineKeyboardButton(text=f"{E_['browse']} BROWSE", callback_data="browse"),
         InlineKeyboardButton(text=f"{E_['library']} MY LIBRARY", callback_data="library")],

        [InlineKeyboardButton(text=f"{E_['age']} BY AGE", callback_data="browse:age"),
         InlineKeyboardButton(text=f"{E_['studio']} BY STUDIO", callback_data="browse:studio"),
         InlineKeyboardButton(text=f"{E_['era']} BY ERA", callback_data="browse:era")],

        [InlineKeyboardButton(text="7–9", callback_data="age:7-9"),
         InlineKeyboardButton(text="10–12", callback_data="age:10-12"),
         InlineKeyboardButton(text="13–14", callback_data="age:13-14"),
         InlineKeyboardButton(text="15–17", callback_data="age:15-17")],

        [InlineKeyboardButton(text=f"{E_['ethnicity']} ETHNICITY", callback_data="browse:ethnicity"),
         InlineKeyboardButton(text=f"{E_['featured']} FEATURED", callback_data="featured"),
         InlineKeyboardButton(text=f"{E_['full_sets']} FULL SETS", callback_data="full_sets")],

        [InlineKeyboardButton(text=f"{E_['new']} NEW", callback_data="new"),
         InlineKeyboardButton(text=f"{E_['top']} TOP", callback_data="top"),
         InlineKeyboardButton(text=f"{E_['rare']} RARE", callback_data="rare")],

        [InlineKeyboardButton(text=f"{E_['search']} SEARCH", callback_data="search"),
         InlineKeyboardButton(text=f"{E_['tags']} TAGS", callback_data="tags"),
         InlineKeyboardButton(text=f"{E_['quality']} QUALITY", callback_data="quality")],

        [InlineKeyboardButton(text=f"{E_['purchases']} PURCHASES", callback_data="purchases"),
         InlineKeyboardButton(text=f"{E_['credits']} CREDITS", callback_data="credits"),
         InlineKeyboardButton(text=f"{E_['codes']} CODES", callback_data="codes")],

        [InlineKeyboardButton(text=f"{E_['sources']} SOURCES", callback_data="sources"),
         InlineKeyboardButton(text=f"{E_['trust']} TRUST", callback_data="trust"),
         InlineKeyboardButton(text=f"{E_['how']} HOW IT WORKS", callback_data="how")],

        [InlineKeyboardButton(text=f"{E_['channel']} CHANNEL", url="https://t.me/your_channel"),
         InlineKeyboardButton(text=f"{E_['refer']} REFER & EARN", callback_data="refer"),
         InlineKeyboardButton(text=f"{E_['admin']} ADMIN", callback_data="admin")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


main_menu = main_menu_kb