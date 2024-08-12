class Messages:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        """
        Adds a new message to the messages array.

        Args:
            role (str): The role of the sender ('user' or 'assistant').
            content: The content of the message.
        """
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        """
        Returns the list of messages.

        Returns:
            list: The list of messages.
        """
        return self.messages

    def save_messages(self,new_messages_array):
        self.messages = new_messages_array

    def clear_messages(self):
        """
        Clears the list of messages.
        """
        self.messages = []