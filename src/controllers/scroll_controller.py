import time

from utils.defines import STOPPED_MAX
STEP = 500

class ScrollController:
 
    @staticmethod
    def scroll_up(driver, scroll_area, step=STEP, max_scroll_time=STOPPED_MAX):

        if not scroll_area:
            print("스크롤 영역을 찾을 수 없습니다.")
            return
        
        start_time = time.time()
        prev_top = None
        while True:
            current_top = driver.execute_script("return arguments[0].scrollTop;", scroll_area)
            
            if time.time() - start_time >= max_scroll_time:
                print(f"{max_scroll_time}초 경과, 스크롤 중단")
                break
        
            if current_top == 0 or current_top == prev_top:
                print("화면 맨 위 도착!")
                break
            
            # 테스트 용 ===================================
            print(f"[up] current_top :{current_top} == prev_top :{prev_top} ?")
            #  ==========================================
    
            driver.execute_script(
                "arguments[0].scrollBy(0, arguments[1]);",
                scroll_area, -step
            )
            time.sleep(0.3)
            prev_top = current_top

    @staticmethod
    def scroll_down(driver, scroll_area, step=STEP):

        if not scroll_area:
            print("스크롤 영역을 찾을 수 없습니다.")
            return

        prev_btm = None
        while True:
            current_btm = driver.execute_script("return arguments[0].scrollTop;", scroll_area)
            height = driver.execute_script("return arguments[0].scrollHeight;", scroll_area)

            if current_btm + scroll_area.size["height"] >= height:
                print("화면 맨 아래 도착!")
                break
            
            if current_btm == prev_btm:
                print("화면 맨 아래 도착!")
                break
            
            # 테스트 용 ====================================
            print(f"[down] current_btm :{current_btm} + scroll_area.size['height']: {scroll_area.size['height']} >= scroll_height :{height} ?")
            #  ==========================================
        
            driver.execute_script(
                "arguments[0].scrollBy(0, arguments[1]);",
                scroll_area, step
            )
            time.sleep(0.3)
            prev_btm = current_btm
            
