import os
import time

# 성진 - 다운로드 파일이 잘 되는지 확인해보려고 넣어놨습니다!
def is_file_downloaded(filename, timeout=10):
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    target_path = os.path.join(download_dir, filename)

    end_time = time.time() + timeout
    while time.time() < end_time:
        if os.path.exists(target_path):
            return True
        time.sleep(0.5)
    return False

def wait_for_download(download_dir, filename, timeout=10):
    end_time = time.time() + timeout
    while time.time() < end_time:
        for f in os.listdir(download_dir):
            if filename in f:
                return True
        time.sleep(0.5)
    return False

def wait_for_download_contains(download_dir, keyword="", ext="", timeout=20):
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = os.listdir(download_dir)

        # 크롬 다운로드 중 파일(.crdownload) 제외하고 보려면
        files = [f for f in files if not f.endswith(".crdownload")]

        for f in files:
            if (keyword in f) and (ext == "" or f.lower().endswith(ext.lower())):
                return f  # 실제 파일명 반환
        time.sleep(0.5)
    return None