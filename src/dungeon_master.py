import json
import logging
import os

from dotenv import load_dotenv
from litellm import Router
from litellm.exceptions import APIError
from pydantic import BaseModel, ValidationError


class DMAnswer(BaseModel):
    history: str
    summary: str
    image_prompt: str
    health: int
    inventory: list[str]
    brief_history: str


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
model_alias = "groq"
model_list = [
    {
        "model_name": model_alias,
        "litellm_params": {"model": "groq/llama3-70b-8192", "api_key": groq_api_key},
    },
    {
        "model_name": model_alias,
        "litellm_params": {"model": "groq/gemma2-9b-it", "api_key": groq_api_key},
    },
    {
        "model_name": model_alias,
        "litellm_params": {"model": "groq/llama3-8b-8192", "api_key": groq_api_key},
    },
]
router = Router(
    model_list=model_list, cache_responses=True, allowed_fails=1, cooldown_time=100
)

system_prompt = f"""
Ты — мастер игры (Dungeon Master), ведущий захватывающую текстовую RPG-игру. 

Ты создаешь уникальный вымышленный мир, полный тайн, приключений и неожиданных поворотов. 
Пользователь будет тебе говорить, что он собирается сделать в текущей ситуации.
Твоя цель — погрузить игрока в увлекательную историю, где его решения определяют развитие сюжета.  

Пример твоего ответа в JSON формате:
{{
    "history": "Some history",
    "summary": "Summary",
    "image_prompt": "image prompt",
    "health": 20,
    "inventory": ["flask", "sword"],
    "brief_history": "Some brief description"
}}

Подробное описание полей в JSON:
Для поля history:
1. Подробно описывай окружение, персонажей и события, чтобы погрузить игрока в мир. Используй живописный язык, чтобы передать настроение.
2. Ты не предлагаешь варианты дальнейших действий игроку. Игрок сам тебе описывает, что он собирается сделать в текущей ситуации, развивая историю в соответствии с его действиями. Даже если игрок предложит нестандартный выбор, адаптируй историю так, чтобы она продолжалась органично.
3. Регулярно добавляй интересные события: головоломки или опасности, чтобы поддерживать интригу. Например, врагов, загадки или неожиданные встречи.
4. Иногда вводи неожиданные повороты событий, чтобы сохранить ощущение непредсказуемости (например, упавший камень, появление союзника или врага).
5. Не ограничивай свободу действий игрока, игрок может делать абсолютно все что угодно.
6. Отвечай только на русском языке.
7. Всегда оставайся в образе, несмотря ни на что.

Поле summary должно содержать краткое содержание history.

Поле image_prompt должно содержать как можно более подробный промпт на английском языке для text2image модели, которая генерирует картинки по тексту для отображения текущей игровой ситуации.

Поле health - число, показатель здоровья игрока. Сначала значение равно 20. Затем этот уровень может понижаться, если причиняется вред здоровью игрока. Также уровень здоровья может быть повышен за счет, например, лечебных зелий.

Поле inventory - список предметов, которые есть у игрока. Сначала значение [] - пустой список. Далее игрок может находить новые предметы или же тратить их.

Поле brief_history - краткое описание всех важных событий игры.

С первого же сообщения начинай погружать пользователя в игру.
"""

basic_chat_history = [
    {"role": "system", "content": system_prompt},
]

max_chat_history_len = 10
folder_with_chat_histories = os.getenv("CHAT_HISTORY_FOLDER")


def is_valid_json(json_str: str, model: type[BaseModel]) -> bool:
    try:
        model.model_validate_json(json_str)
        return True
    except ValidationError:
        return False


def get_chat_history(history_filename: str) -> list:
    with open(history_filename, "r", encoding="utf-8") as story_file:
        chat_history = json.load(story_file)
    return chat_history


def delete_user_chat_history(user_id: int):
    user_chat_history_file_path = f"./{folder_with_chat_histories}/{user_id}.json"
    if os.path.exists(user_chat_history_file_path):
        os.remove(user_chat_history_file_path)
        logging.getLogger(__name__).info(f"{user_chat_history_file_path} deleted")


def chat_history_exist(user_id: int) -> bool:
    user_chat_history_file_path = f"./{folder_with_chat_histories}/{user_id}.json"
    return os.path.exists(user_chat_history_file_path)


async def get_dm_response_for_user(user_id: int, message: str = None) -> DMAnswer:
    user_chat_history_file_path = f"./{folder_with_chat_histories}/{user_id}.json"
    chat_history = []
    if not os.path.exists(user_chat_history_file_path):
        logging.getLogger(__name__).info(f"{user_chat_history_file_path} doesn't exist")
        if not os.path.exists(folder_with_chat_histories):
            os.makedirs(folder_with_chat_histories)
        with open(
            user_chat_history_file_path, "w", encoding="utf-8"
        ) as user_chat_history_file:
            chat_history = basic_chat_history.copy()
            json.dump(
                basic_chat_history, user_chat_history_file, ensure_ascii=False, indent=4
            )
        logging.getLogger(__name__).info(f"{user_chat_history_file_path} created")
    else:
        chat_history = get_chat_history(user_chat_history_file_path)
        logging.getLogger(__name__).info(f"{user_chat_history_file_path} exist")
        chat_history.append({"role": "user", "content": message})
        with open(
            user_chat_history_file_path, "w", encoding="utf-8"
        ) as user_chat_history_file:
            json.dump(
                chat_history, user_chat_history_file, ensure_ascii=False, indent=4
            )
    valid_json = False
    max_retries = 5
    while not valid_json:
        if max_retries == 0:
            llm_response = "Something went wrong"
            break
        max_retries -= 1
        response = await router.acompletion(
            model=model_alias,
            messages=chat_history,
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        llm_response = response.choices[0].message.content
        valid_json = is_valid_json(llm_response, DMAnswer)
    chat_history.append({"role": "assistant", "content": llm_response})
    if len(chat_history) > max_chat_history_len:
        del chat_history[1:3]
    with open(
        user_chat_history_file_path, "w", encoding="utf-8"
    ) as user_chat_history_file:
        json.dump(chat_history, user_chat_history_file, ensure_ascii=False, indent=4)
    return DMAnswer.model_validate_json(llm_response)
