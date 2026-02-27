import curses

def draw(stdscr, width, height, ground_y, p_units, e_units, gold, p_hp, e_hp, 
         army_lv, _unused_dmg_lv, upgrade_cost, _unused_dmg_cost, show_promo_mode, s_type, a_type, k_type, ai_s, ai_a, ai_k):
    """
    k_type: 기병의 현재 타입 ("@", "C", "W") 인자를 추가로 받아야 합니다.
    """
    # 1. 화면 초기화
    stdscr.clear()

    # 2. 상단 기본 UI
    stdscr.addstr(0, 2, f"GOLD: {gold}G  |  BASE: {p_hp} vs {e_hp}", curses.color_pair(3))
    stdscr.addstr(1, 2, f"[9] Army Training Lv.{army_lv} ({upgrade_cost}G)", curses.color_pair(3) | curses.A_BOLD)
    ai_info_x = width - 25
    stdscr.addstr(1, ai_info_x, "  [ AI INTEL ]", curses.color_pair(2))
    
    # AI 보병 정보

    # --- AI 유닛 이름 매핑 ---
    # 보병(Infantry) 이름 매핑 (스파르타 'T' 추가)
    inf_names = {"#": "Soldier", "S": "Spearman", "P": "Paladin", "T": "Sparta"}
    # 궁수(Archer) 이름 매핑
    arc_names = {"&": "Archer", "M": "Musketeer", "J": "Javelin", "F": "Fire Archer"}
    # 기병(Cavalry) 이름 매핑
    cav_names = {"@": "Knight", "C": "Chariot", "W": "W.Hussar", "D": "Dragoon"}

    # 이름 결정 (매핑에 없는 경우 기본값 설정)
    s_name = inf_names.get(ai_s, "Unknown")
    a_name = arc_names.get(ai_a, "Unknown")
    k_name = cav_names.get(ai_k, "Unknown")

    # 상단 AI 정보 출력 (색상: 빨간색/2번 페어)
    stdscr.addstr(2, ai_info_x, f"Inf: {ai_s} ({s_name:8s})", curses.color_pair(2))
    stdscr.addstr(3, ai_info_x, f"Arc: {ai_a} ({a_name:8s})", curses.color_pair(2))
    stdscr.addstr(4, ai_info_x, f"Cav: {ai_k} ({k_name:8s})", curses.color_pair(2))
    
    # --- [동적 UI] 1. 보병 설정 ---
    if s_type == "#":
        s_display = "Soldier (#): 4G"
        stdscr.addstr(3, 2, "[5] Promote Soldier (20G)", curses.color_pair(3))
    elif s_type == "S":
        s_display = "Spearman (S): 4G"
        stdscr.addstr(3, 2, "RANK UP: Spearman Active!", curses.color_pair(1))
    elif s_type == "T":
        s_display = "Sparta (T): 6G"
        stdscr.addstr(3, 2, "RANK UP: Sparta Active!", curses.color_pair(1))
    else: # "P"
        s_display = "Paladin (P): 6G"
        stdscr.addstr(3, 2, "RANK UP: Paladin Active!", curses.color_pair(1))

    # --- [동적 UI] 2. 궁수 설정 ---
    if a_type == "&":
        a_display = "Archer (&): 6G"
        # 보병 전직이 완료된 후에만 궁수 전직 가이드 표시
        if s_type != "#":
            stdscr.addstr(4, 2, "[5] Promote Archer (25G)", curses.color_pair(3))
    elif a_type == "M":
        a_display = "Musketeer (M): 8G"
        stdscr.addstr(4, 2, "RANK UP: Musketeer Active!", curses.color_pair(1))
    elif a_type == "F": # 불화살 사수 디스플레이 추가
        a_display = "FireArc (F): 7G"
        stdscr.addstr(4, 2, "RANK UP: Fire Archer Active!", curses.color_pair(1))
    else: # "J"
        a_display = "Javelin (J): 6G"
        stdscr.addstr(4, 2, "RANK UP: Javelin Active!", curses.color_pair(1))

    # --- [동적 UI] 3. 기병 설정 (새로 추가) ---
    if k_type == "@":
        k_display = "Knight (@): 14G"
        # 궁수 전직까지 완료된 후에만 기병 전직 가이드 표시
        if a_type != "&":
            stdscr.addstr(5, 2, "[5] Promote Knight (30G)", curses.color_pair(3))
    elif k_type == "C":
        k_display = "Chariot (C): 20G"
        stdscr.addstr(5, 2, "RANK UP: Chariot Active!", curses.color_pair(1))
    elif k_type == "W": # "W"
        k_display = "W.Hussar (W): 18G"
        stdscr.addstr(5, 2, "RANK UP: W.Hussar Active!", curses.color_pair(1))
    elif k_type == "D":
        k_display = "Dragoon (D): 18G"
        stdscr.addstr(5, 2, "RANK UP: Dragoon Active!", curses.color_pair(1))

    # 오른쪽 생산 메뉴 출력 (현재 유닛 타입 반영)
    stdscr.addstr(1, 35, f"[1] {s_display}")
    stdscr.addstr(2, 35, f"[2] {a_display}")
    stdscr.addstr(3, 35, f"[3] {k_display}")
    
    stdscr.addstr(0, width - 18, f"AI BASE: {e_hp}", curses.color_pair(2))

    # 3. 바닥 및 베이스
    for x in range(width - 1):
        try: stdscr.addstr(ground_y, x, "-")
        except: pass
    stdscr.addstr(ground_y - 1, 2, "P", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(ground_y - 1, width - 3, "A", curses.color_pair(2) | curses.A_BOLD)

    # 4. 유닛 그리기
    for u in p_units + e_units:
        x_pos = max(0, min(width - 2, int(u.x)))
        char = u.kind
        if u.kind in ["&", "M", "J","F","D"] and u.state_timer > 0:
            char = "$" # 원거리 공격 연출
        
        color = curses.color_pair(1) if u.team == "player" else curses.color_pair(2)
        try: stdscr.addstr(ground_y - 1, x_pos, char, color | curses.A_BOLD)
        except: pass

    # 5. 전직 선택 팝업창
    if show_promo_mode > 0:
        win_h, win_w = 9, 46
        start_y, start_x = height // 2 - 4, width // 2 - 23
        # 테두리 그리기
        for y in range(win_h):
            for x in range(win_w):
                if y == 0 or y == win_h-1: char = "="
                elif x == 0 or x == win_w-1: char = "|"
                else: char = " "
                stdscr.addstr(start_y+y, start_x+x, char, curses.color_pair(3))

        if show_promo_mode == 1:
            stdscr.addstr(start_y + 1, start_x + 12, "--- SOLDIER PROMOTION ---", curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(start_y + 3, start_x + 3, "[6] Spearman: Anti Knights, Range 2 (4G)", curses.color_pair(1))
            stdscr.addstr(start_y + 4, start_x + 3, "[7] Paladin : HP 25, DMG 6   (6G)", curses.color_pair(1))
            stdscr.addstr(start_y + 5, start_x + 3, "[8] Sparta  : HP 33, DMG 5   (6G)", curses.color_pair(1))
            stdscr.addstr(start_y + 7, start_x + 16, "COST: 20 GOLD", curses.color_pair(2))
        elif show_promo_mode == 2:
            stdscr.addstr(start_y + 1, start_x + 13, "--- ARCHER PROMOTION ---", curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(start_y + 3, start_x + 3, "[6] Musketeer: DMG 8, Range 6 (8G)", curses.color_pair(1))
            stdscr.addstr(start_y + 4, start_x + 3, "[7] Javelin  : Fast Attack     (6G)", curses.color_pair(1))
            stdscr.addstr(start_y + 5, start_x + 3, "[8] Fire Arc : 10% MaxHP Dmg   (7G)", curses.color_pair(1))
            stdscr.addstr(start_y + 7, start_x + 16, "COST: 25 GOLD", curses.color_pair(2))
        elif show_promo_mode == 3:
            stdscr.addstr(start_y + 1, start_x + 13, "--- KNIGHT PROMOTION ---", curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(start_y + 3, start_x + 3, "[6] Chariot: HP 60, Fast Atk (20G)", curses.color_pair(1))
            stdscr.addstr(start_y + 4, start_x + 3, "[7] W.Hussar: DMG 18, Range 3 (17G)", curses.color_pair(1))
            stdscr.addstr(start_y + 5, start_x + 3, "[8] Dragoon: Gun and Sword (18G)", curses.color_pair(1))
            stdscr.addstr(start_y + 7, start_x + 16, "COST: 30 GOLD", curses.color_pair(2))

    stdscr.refresh()