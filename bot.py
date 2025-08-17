import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters.command import Command
from aiogram import Router
from aiogram import F

logging.basicConfig(level=logging.INFO)

bot = Bot(token='YOUR_BOT_TOKEN')
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Hello, main All in One Calculator bot hoon. Main various calculations mein madad kar sakta hoon. Yahan commands ki list hai:\n"
        "/loan - Loan Calculator kholo\n"
        "/bmi - BMI Calculator kholo\n"
        "/area - Area Calculator kholo\n"
        "/data - Data Converter kholo\n"
        "/discount - Discount Calculator kholo\n"
        "/length - Length Converter kholo\n"
        "/mass - Mass Converter kholo\n"
        "/numeral - Numeral System Converter kholo\n"
        "/speed - Speed Converter kholo\n"
        "/temp - Temperature Converter kholo\n"
        "/time - Time Converter kholo\n"
        "/volume - Volume Calculator kholo"
    )

async def open_calc_handler(message: types.Message, calc: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Open {calc.capitalize()} Calculator", web_app=WebAppInfo(url=f"http://t.me/TechYYrom_bot/Techyy?start={calc}"))]
    ])
    await message.answer(f"{calc.capitalize()} Calculator khol raha hoon...", reply_markup=keyboard)

@router.message(Command("loan"))
async def loan_handler(message: types.Message):
    await open_calc_handler(message, "loan")

@router.message(Command("bmi"))
async def bmi_handler(message: types.Message):
    await open_calc_handler(message, "bmi")

@router.message(Command("area"))
async def area_handler(message: types.Message):
    await open_calc_handler(message, "area")

@router.message(Command("data"))
async def data_handler(message: types.Message):
    await open_calc_handler(message, "data")

@router.message(Command("discount"))
async def discount_handler(message: types.Message):
    await open_calc_handler(message, "discount")

@router.message(Command("length"))
async def length_handler(message: types.Message):
    await open_calc_handler(message, "length")

@router.message(Command("mass"))
async def mass_handler(message: types.Message):
    await open_calc_handler(message, "mass")

@router.message(Command("numeral"))
async def numeral_handler(message: types.Message):
    await open_calc_handler(message, "numeral")

@router.message(Command("speed"))
async def speed_handler(message: types.Message):
    await open_calc_handler(message, "speed")

@router.message(Command("temp"))
async def temp_handler(message: types.Message):
    await open_calc_handler(message, "temp")

@router.message(Command("time"))
async def time_handler(message: types.Message):
    await open_calc_handler(message, "time")

@router.message(Command("volume"))
async def volume_handler(message: types.Message):
    await open_calc_handler(message, "volume")

if __name__ == "__main__":
    dp.run_polling(bot)
