class Group:
    def __init__(self, name, user):
        self.name = name
        self.users = [user]
    def add_member(self, user):
        self.users.append(user)
        return "You joined the group"
    def remove_member(self, user):
        try:
            self.users.remove(user)
            return "You left the group"
        except ValueError:
            return "You arent in that group"
