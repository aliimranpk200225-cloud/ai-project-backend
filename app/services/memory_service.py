class MemoryService:

    def __init__(self):
        self.sessions = {}

    def get_history(self, session_id):

        return self.sessions.get(session_id, [])

    def add_user_message(self, session_id, message):

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({
            "role": "user",
            "content": message
        })

    def add_ai_message(self, session_id, message):

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({
            "role": "assistant",
            "content": message
        })

memory_service = MemoryService()