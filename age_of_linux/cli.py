import curses

from .game import run

def show_controls(stdscr):
    """조작법 및 전직 시스템 안내 화면"""
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # 타이틀
        stdscr.addstr(h//2 - 8, w//2 - 10, "--- HOW TO PLAY ---", curses.color_pair(1) | curses.A_BOLD)
        
        # 기본 조작법
        basic_controls = [
            "  [1, 2, 3] : Spawn Units (Infantry, Archer, Knight)",
            "  [Q]       : Quit Game",
            ""
        ]
        
        # 전직 시스템 (강조)
        promo_info = [
            "--- PROMOTION SYSTEM ---",
            "  [5]       : Open/Close Promotion Menu",
            "  └─ After [5], press [6, 7, 8] to select your path!",
            "     (e.g., 5 -> 6: Become a Spearman)",
            ""
        ]
        
        # 스페셜 유닛
        special_info = [
            "--- SPECIAL UNITS ---",
            "  [4]       : Open Special Menu (Ronin/Fenrir)",
            "  └─ After [4], press [6, 7] to Unlock or Select",
            "  └─ Once selected, press [4] again to spawn them!"
        ]

        # 화면 출력 (중앙 정렬)
        current_row = h//2 - 6
        for text in basic_controls:
            stdscr.addstr(current_row, w//2 - 25, text)
            current_row += 1
            
        for text in promo_info:
            stdscr.addstr(current_row, w//2 - 25, text, curses.color_pair(2) if "6, 7, 8" in text else curses.A_NORMAL)
            current_row += 1
            
        for text in special_info:
            stdscr.addstr(current_row, w//2 - 25, text, curses.color_pair(3) if "Ronin" in text else curses.A_NORMAL)
            current_row += 1

        stdscr.addstr(h - 3, w//2 - 15, "Press any key to return...", curses.A_DIM)
            
        stdscr.refresh()
        stdscr.getch()
        break

def main_menu(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK) # 타이틀
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # 전직 강조
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # 스페셜 강조
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # 하드 모드
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # 일반 텍스트
    
    curses.curs_set(0)
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        title = "AGE OF LINUX"
        stdscr.addstr(h//2 - 6, w//2 - len(title)//2, title, curses.color_pair(1) | curses.A_BOLD)
        
        stdscr.addstr(h//2 - 3, w//2 - 17, "SELECT OPTION [1, 2, 3, 4]", curses.A_UNDERLINE)

        # 메뉴
        stdscr.addstr(h//2 + 0, w//2 - 20, "[1] EASY   - Relaxed game", curses.color_pair(2))
        stdscr.addstr(h//2 + 1, w//2 - 20, "[2] MEDIUM - Normal mode", curses.color_pair(3))
        stdscr.addstr(h//2 + 2, w//2 - 20, "[3] HARD   - Original", curses.color_pair(4))
        stdscr.addstr(h//2 + 4, w//2 - 20, "[4] HOW TO PLAY & CONTROLS", curses.A_BOLD | curses.A_REVERSE)

        stdscr.addstr(h - 2, w//2 - 10, "Press [Q] to Quit", curses.A_DIM)
        
        stdscr.refresh()
        key = stdscr.getch()

        if key == ord('1'):
            run(stdscr, difficulty="Easy")
        elif key == ord('2'):
            run(stdscr, difficulty="Medium")
        elif key == ord('3'):
            run(stdscr, difficulty="Hard")
        elif key == ord('4'):
            show_controls(stdscr)
        elif key in [ord('q'), ord('Q')]:
            break

def main():
    curses.wrapper(main_menu)


if __name__ == "__main__":
    main()
