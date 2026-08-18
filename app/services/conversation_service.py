class ConversationService:

    def __init__(self):
        self.conversations = {}

    def get_history(self, conversation_id):
        return self.conversations.get(
            conversation_id,
            []
        )

    def add_message(
        self,
        conversation_id,
        role,
        content
    ):
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        self.conversations[conversation_id].append({
            "role": role,
            "content": content
        })

    def clear_history(self, conversation_id):
        self.conversations.pop(
            conversation_id,
            None
        )