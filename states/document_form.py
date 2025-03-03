from aiogram.fsm.state import State, StatesGroup

class DocumentForm(StatesGroup):
    date = State()
    link = State()
    social_network = State()
    performer_type = State()
    channel_name = State()
    format = State()
    cost = State()
    performer_documents = State()
    performer_name = State()
    client_name = State()
    client_type = State()
    client_documents = State()
    is_marked = State()
    confirmation = State()