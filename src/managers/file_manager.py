from utils.headers import *

import os
import requests

from utils.defines import TARGET_URL

from controllers.clipboard_controller import ClipboardController

class FileManager:
    def __init__(self):
        # 현재 managers 폴더 경로
        current_dir = os.path.dirname(__file__)  # src/managers
        
        # src 폴더 경로
        self.src_dir = os.path.abspath(os.path.join(current_dir, ".."))  # src 폴더 기준
        
        self.testdata_dir = os.path.join(self.src_dir, "resources", "testdata")
        self.assets_dir = os.path.join(self.src_dir, "resources", "assets")

        project_root = os.path.abspath(os.path.join(self.src_dir, ".."))
        
        self.report_log_dir = os.path.join(project_root, "reports", "logs")
        self.report_screenshot_dir = os.path.join(project_root, "reports", "screenshots")

    # =================== 파일 가져오기 =========================
    def get_asset_path(self, file_name: str):
        return os.path.join(self.assets_dir, file_name)
    
    def get_asset_files(self, extensions=None):
        files = os.listdir(self.assets_dir)

        if extensions:
            files = [f for f in files if f.lower().endswith(extensions)]

        return [os.path.join(self.assets_dir, f) for f in files]
    
    # =================== 파일 읽기 및 쓰기 =========================
    def read_json_file(self, file_name:str):
        file_path = os.path.join(self.testdata_dir, file_name)
        try: 
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"{file_path} 파일을 찾을 수 없음")
            return None
        except json.JSONDecodeError:
            print(f"{file_path} 파일이 올바른 JSON 형식이 아님")
            return None
    
    def save_json_file(self, file_name:str, data):
        file_path = os.path.join(self.testdata_dir, file_name)
        try: 
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"{file_path} 저장 완료!!")
        except Exception as e:
            print(f"{file_path} 저장 실패!: {e}")
            
        # 로그를 어떻게 적을지, 로그 형식(날짜, 작성자, 내용 등) 정한 후에 
    def save_log_file_to_csv(self, file_name, file_data, option="w"):
        if not file_name.endswith(".csv"):
            file_name += ".csv"
            
        file_path = os.path.join(self.report_log_dir, file_name)

        if not file_data:
            print(f"저장할 데이터가 없음: {file_path}")
            return

        fieldnames = list(file_data[0].keys())

        with open(file_path, option, encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(file_data)

        print(f"CSV 저장 완료: {file_path}")

    # =================== 스크린샷 =========================
    def save_screenshot_png(self, mydriver, file_name: str):    
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        file_name_with_ts = f"{file_name}_{timestamp}.png"
        file_path = os.path.join(self.report_screenshot_dir, file_name_with_ts)

        mydriver.save_screenshot(file_path)
        print(f"Screenshot saved: {file_path}")

        return file_path 
