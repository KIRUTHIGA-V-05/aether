class ContextManager:
    def __init__(self):
        self.history = []
        self.last_entity = None
        self.active_mode = "BOARD"

    def update_context(self, intent, entity):
        self.history.append({"intent": intent, "entity": entity})
        if entity:
            self.last_entity = entity
        if len(self.history) > 10:
            self.history.pop(0)

    def resolve_references(self, text):
        if any(ref in text.lower() for ref in ["this", "that", "it", "above"]):
            return self.last_entity if self.last_entity else text
        return text

context_manager = ContextManager()