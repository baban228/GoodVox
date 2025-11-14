from enum import IntEnum
from telegram import Update
from telegram.ext import ContextTypes


class StateType(IntEnum):
    '''Тут пишутся новые состояния в таком формате, остальное можно не знать'''
    MAIN_MENU = 0
    TEXT_GEN = 1
    IMAGE_GEN = 2
    COR_TEXT = 3
    PLAN = 4


class State:
    def __init__(self, state_type: int):
        self.st: int = state_type
        self.sub_states: list['State'] = []

    def add_sub_state(self, sub_state: 'State'):
        self.sub_states.append(sub_state)


class StateMachine:
    def __init__(self):
        self.current_state: State = None

    def set_state(self, new_state: 'State'):
        self.current_state = new_state

#состояние меняет
async def set_user_state(update: Update, context: ContextTypes.DEFAULT_TYPE, state_type: StateType):
    user_id = update.effective_user.id
    if 'user_states' not in context.bot_data:
        context.bot_data['user_states'] = {}

    context.bot_data['user_states'][user_id] = state_type