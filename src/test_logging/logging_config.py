import logging, os

def setup_logging():
    current_dir = os.path.dirname(__file__)           # .../ai-heplychat-automation/src
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    # .../ai-heplychat-automation

    log_dir = os.path.join("reports", "logs") #src 외부임
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, "run.log")
    print(">>> run.log path:", log_path)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s:%(funcName)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )