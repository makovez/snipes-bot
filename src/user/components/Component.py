
class Component:
    def __init__(self, session, user_id, logger):
        """Define basic structure of each component
        """
        self.session = session
        self.user_id = user_id
        self.logger = logger

