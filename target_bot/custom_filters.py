from telegram.ext.filters import MessageFilter


class TargetUserFilter(MessageFilter):
    def __init__(self, user_id):
        self.user_id = int(user_id)

    def filter(self, message):
        return message.from_user.id == self.user_id


class AllowedUserFilter(TargetUserFilter):
    def filter(self, message):
        return not (message.from_user.id == self.user_id)
