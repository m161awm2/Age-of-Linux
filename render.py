import curses

def draw(stdscr, width, height, ground_y, p_units, e_units, gold, p_hp, e_hp, hp_lv, dmg_lv, hp_cost, dmg_cost):
    # 1. 화면 초기화
    stdscr.clear()

    # 색상 쌍 설정 (game.py의 run 함수 시작 부분에서 초기화 필요)
    # 1: 노랑(플레이어), 2: 빨강(AI), 3: 초록(UI/기타)
    
    # 2. 상단 UI
    stdscr.addstr(0, 2, f"GOLD: {gold}G  |  BASE: {p_hp} vs {e_hp}", curses.color_pair(3))
    stdscr.addstr(1, 2, f"[9] HP  Lv.{hp_lv} ({hp_cost}G)")
    stdscr.addstr(2, 2, f"[0] DMG Lv.{dmg_lv} ({dmg_cost}G)")
    stdscr.addstr(1, 30, f"[1] Soldier (#): 4G")
    stdscr.addstr(2, 30, f"[2] Archer  (&): 6G")
    stdscr.addstr(3, 30, f"[3] Knight  (@): 14G")
    stdscr.addstr(0, width - 15, f"AI BASE: {e_hp}", curses.color_pair(2))

    # 3. 바닥 (Ground)
    for x in range(width - 1):
        try:
            stdscr.addstr(ground_y, x, "-")
        except: pass

    # 4. 베이스 위치 표시 (색상 적용)
    stdscr.addstr(ground_y - 1, 2, "P", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(ground_y - 1, width - 3, "A", curses.color_pair(2) | curses.A_BOLD)

    # 5. 유닛 그리기
    for u in p_units + e_units:
        x_pos = max(0, min(width - 2, int(u.x)))
        
        char = u.kind
        if u.kind == "&" and u.state_timer > 0:
            char = "$"
        
        # 팀에 따른 색상 선택
        color = curses.color_pair(1) if u.team == "player" else curses.color_pair(2)
        
        try:
            # 유닛 출력 시 색상 적용
            stdscr.addstr(ground_y - 1, x_pos, char, color | curses.A_BOLD)
        except: pass

    # 6. 화면 갱신
    stdscr.refresh()
