# handlers.py
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sheets import get_managers, get_all_brands, get_categories_by_brand, get_products_by_brand_and_category, save_order

router = Router()

user_state = {}  # Temporarily store user step

@router.message(CommandStart())
async def start_cmd(message: types.Message):
    keyboard = [
        [InlineKeyboardButton(text=name, callback_data=f"manager:{name}")]
        for name in get_managers()
    ]
    await message.answer("Menejeringizni tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

@router.callback_query(F.data.startswith("manager:"))
async def select_manager(callback: types.CallbackQuery):
    manager = callback.data.split(":")[1]
    user_state[callback.from_user.id] = {"manager": manager}
    brands = get_all_brands()
    keyboard = [[InlineKeyboardButton(text=b, callback_data=f"brand:{b}")] for b in brands]
    await callback.message.edit_text("Brendni tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

@router.callback_query(F.data.startswith("brand:"))
async def select_brand(callback: types.CallbackQuery):
    brand = callback.data.split(":")[1]
    user_state[callback.from_user.id]["brand"] = brand
    categories = get_categories_by_brand(brand)
    keyboard = [[InlineKeyboardButton(text=c, callback_data=f"category:{c}")] for c in categories]
    await callback.message.edit_text("Kategoriya tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

@router.callback_query(F.data.startswith("category:"))
async def select_category(callback: types.CallbackQuery):
    category = callback.data.split(":")[1]
    data = user_state[callback.from_user.id]
    data["category"] = category
    products = get_products_by_brand_and_category(data["brand"], category)
    keyboard = [[InlineKeyboardButton(text=p, callback_data=f"product:{p}")] for p in products]
    await callback.message.edit_text("Mahsulot tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

@router.callback_query(F.data.startswith("product:"))
async def select_product(callback: types.CallbackQuery):
    product = callback.data.split(":")[1]
    user_state[callback.from_user.id]["product"] = product
    await callback.message.edit_text("Nechta dona buyurtma berilsin? (raqam kiriting):")

@router.message(F.text.regexp(r'^\d+$'))
async def quantity_input(message: types.Message):
    user_state[message.from_user.id]["quantity"] = message.text
    await message.answer("Sana kiriting (masalan, 2025-07-12):")

@router.message(F.text.regexp(r'^\d{4}-\d{2}-\d{2}$'))
async def date_input(message: types.Message):
    user_state[message.from_user.id]["date"] = message.text
    await message.answer("Izoh kiriting (yoki '-' yozing):")

@router.message()
async def comment_input(message: types.Message):
    state = user_state.get(message.from_user.id)
    if not state:
        await message.answer("Iltimos, /start buyrug‘idan boshlang.")
        return
    comment = message.text
    save_order(
        manager=state["manager"],
        brand=state["brand"],
        category=state["category"],
        product=state["product"],
        quantity=state["quantity"],
        date=state["date"],
        comment=comment
    )
    await message.answer("✅ Buyurtma qabul qilindi!\n/start buyrug‘i orqali yangi buyurtma berishingiz mumkin.")
    user_state.pop(message.from_user.id, None)
