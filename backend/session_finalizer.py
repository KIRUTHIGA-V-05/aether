import json
from logger_service import logger
from notice_board_manager import notice_manager

class SessionFinalizer:
    def finalize(self, session_id):
        final_data = {
            "session_id": session_id,
            "teaching_logs": logger.session_data,
            "notice_board_history": notice_manager.get_all_notices(),
            "summary_stats": {
                "total_actions": len(logger.session_data),
                "notice_count": len(notice_manager.active_notices)
            }
        }
        
        filename = f"final_session_{session_id}.json"
        with open(filename, "w") as f:
            json.dump(final_data, f, indent=4)
        
        return filename

finalizer = SessionFinalizer()