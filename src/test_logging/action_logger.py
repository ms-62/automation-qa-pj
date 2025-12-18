from managers.file_manager import FileManager

from test_logging.build_action_log import build_action_log
from utils.context import TextContext, ActionResult

fm = FileManager()  #

def log_action(ctx : TextContext, result: ActionResult, target=""):
    log = build_action_log(ctx, result, target, result.detail)
    file_name = f"{result.action}_log.csv"
    fm.save_log_file_to_csv(file_name, [log])
    
