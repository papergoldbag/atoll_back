from atoll_back.tg_bot.keyboards import SportsmanKeyboard, AdminKeyboard, RepresentativeKeyboard, PartnerKeyboard

def return_user_keyboard(role: str):
    if role == "sportsman":
        return SportsmanKeyboard
    elif role == "admin":
        return AdminKeyboard
    elif role == "representative":
        return RepresentativeKeyboard
    elif role == "partner":
        return PartnerKeyboard