from enum import Enum

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

from processor import PlotWidget

bot = Bot(token="1353236117:AAFqai-3H3yc9bDJgzO_NlY8zExA0FQvu8A")
storage = MemoryStorage()
disp = Dispatcher(bot, storage=storage)
disp.middleware.setup(LoggingMiddleware())

processor_cb = CallbackData("process", "action")  # post:<id>:<action>


class StateMachine(StatesGroup):
    form_input = State()


class Actions(str, Enum):
    PLOTTING = "plotting"


@disp.message_handler(commands=["start", "help"])
async def start_handler(message: types.Message):
    await message.answer("Доступные действия:", reply_markup=get_keyboard())


def get_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "График", callback_data=processor_cb.new(action=Actions.PLOTTING)
        ),
    )
    return markup


@disp.callback_query_handler(processor_cb.filter(action=Actions.PLOTTING))
async def query_show_list(query: types.CallbackQuery):
    await query.message.edit_text("Введите вашу формулу:")
    await StateMachine.form_input.set()


@disp.message_handler(state=StateMachine.form_input)
async def process_plot(message: types.Message, state: FSMContext):
    media = types.MediaGroup()

    try:
        image = PlotWidget().plot(message.text)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return

    await state.finish()

    media.attach_photo(types.InputFile(image))

    await message.reply_media_group(media=media)
    await message.answer("Следующее действие:", reply_markup=get_keyboard())


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)
