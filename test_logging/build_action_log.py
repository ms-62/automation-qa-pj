from datetime import datetime
from utils.context import TextContext, ActionResult

def build_action_log(ctx: TextContext, result: ActionResult, target="", detail=""):
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test_name": ctx.test_name,
        "page": ctx.page,
        "action": result.action,
        "target": target,
        "result": result.result,
        "detail": detail or result.detail,
        "elapsed_time": result.elapsed_time,
        "screenshot": result.screenshot
    }