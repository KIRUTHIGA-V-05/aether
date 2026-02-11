class NoticeBoardManager:
    def __init__(self):
        self.active_notices = []
        self.important_keywords = ["remember", "important", "note", "exam", "deadline"]

    def process_for_notice(self, text: str):
        is_important = any(word in text.lower() for word in self.important_keywords)
        if is_important:
            notice_entry = {
                "content": text,
                "type": "HIGHLIGHT",
                "priority": "HIGH"
            }
            self.active_notices.append(notice_entry)
            return notice_entry
        return None

    def get_all_notices(self):
        return self.active_notices

notice_manager = NoticeBoardManager()