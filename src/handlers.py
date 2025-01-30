import asyncio
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hide_link

from src.dungeon_master import (chat_history_exist, delete_user_chat_history,
                                get_dm_response_for_user)
from text2image import G4FImageGenerator, PollinationsAIGenerator

router: Router = Router()
gf4_image_generator = G4FImageGenerator()
pollinations_ai_generator = PollinationsAIGenerator()


async def generate_answer_for_user(user_id: int, message: str) -> str:
    dm_response = await get_dm_response_for_user(user_id, message)
    logging.getLogger(__name__).info(f"image prompt: {dm_response.image_prompt}")
    # image_url = await gf4_image_generator.generate_image(dm_response.image_prompt)
    image_url = await pollinations_ai_generator.generate_image(dm_response.image_prompt)
    if dm_response.health <= 0:
        dm_response.health = 0
        dm_response.history += " Игра закончена."
        delete_user_chat_history(user_id)
    formatted_dm_response = (
        f"{hide_link(image_url)}"
        f"<b>Здоровье: {dm_response.health}❤️</b>\n"
        f"<b>Инвентарь: {dm_response.inventory}</b>\n\n"
        f"{dm_response.history}\n\n"
    )
    return formatted_dm_response


@router.message(Command("start"))
async def process_start_command(message: Message):
    user_id = message.from_user.id
    delete_user_chat_history(user_id)
    answer = await generate_answer_for_user(user_id, message.text)
    answer = f"<b>Добро пожаловать в llmia! Напишите /start, чтобы начать новую игру.</b>\n\n{answer}"
    await message.reply(text=answer, parse_mode="HTML")


@router.message()
async def process_text_message(message: Message):
    user_id = message.from_user.id
    if not chat_history_exist(user_id):
        answer = "<b>Напишите /start, чтобы начать новую игру.</b>"
    else:
        answer = await generate_answer_for_user(user_id, message.text)
    await message.reply(text=answer, parse_mode="HTML")
