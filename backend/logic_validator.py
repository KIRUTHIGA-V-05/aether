class LogicValidator:
    def __init__(self):
        self.state_rules = {
            "PPT": ["ACTION_PPT_NAV", "ACTION_ANNOTATE"],
            "BOARD": ["ACTION_WRITE", "ACTION_DRAW", "ACTION_TABLE", "ACTION_SOLVE_PATTERN"]
        }

    def validate_command(self, current_mode: str, intent: str):
        if intent == "UNKNOWN":
            return False, "Command not recognized. Please rephrase."
        
        if intent not in self.state_rules.get(current_mode, []):
            return False, f"Action {intent} is not available in {current_mode} mode."
        
        return True, "Validated"

validator = LogicValidator()