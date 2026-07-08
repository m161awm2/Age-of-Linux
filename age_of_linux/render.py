import curses

def draw(stdscr, width, height, ground_y, p_units, e_units, gold, p_hp, e_hp, 
            show_promo_mode, s_type, a_type, k_type, ai_s, ai_a, ai_k, unlocked_units=[],current_special = None):
        """
        k_type: 기병의 현재 타입 ("@", "C", "W") 인자를 추가로 받아야 합니다.
        """
        # 1. 화면 초기화
        stdscr.clear()

        # 2. 상단 기본 UI
        stdscr.addstr(0, 2, f"GOLD: {gold}G  |  BASE: {p_hp} vs {e_hp}", curses.color_pair(3))
        ai_info_x = width - 25
        stdscr.addstr(1, ai_info_x, "  [ AI INTEL ]", curses.color_pair(2))
        
        # AI 보병 정보

        # --- AI 유닛 이름 매핑 ---
        # 보병(Infantry) 이름 매핑
        inf_names = {"#": "Soldier", "S": "Spearman", "H": "Halberd", "P": "Paladin", "U": "Crusader", "T": "Sparta", "G": "Guardian"}
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
        
        if show_promo_mode == 0:
            if current_special == "L":
                stdscr.addstr(height-1, 2, "[4] Spawn Fenrir (4G)", curses.color_pair(1))
            elif current_special == "R":
                stdscr.addstr(height-1, 2, "[4] Spawn Ronin (8G)", curses.color_pair(1))
            elif not current_special:
                stdscr.addstr(height-1, 2, "[4] Special Unit Menu", curses.color_pair(3))
        # --- [동적 UI] 1. 보병 설정 ---
        if s_type == "#":
            s_display = "Soldier (#): 4G"
            stdscr.addstr(3, 2, "[5] Promote Soldier (20G)", curses.color_pair(3))
        elif s_type == "S":
            s_display = "Spearman (S): 4G"
            if a_type != "&" and k_type != "@":
                stdscr.addstr(3, 2, "[5] Promote Spearman (35G)", curses.color_pair(3))
            else:
                stdscr.addstr(3, 2, "RANK UP: Spearman Active!", curses.color_pair(1))
        elif s_type == "H":
            s_display = "Halberd (H): 6G"
            stdscr.addstr(3, 2, "RANK UP: Halberd Active!", curses.color_pair(1))
        elif s_type == "T":
            s_display = "Sparta (T): 6G"
            if a_type != "&" and k_type != "@":
                stdscr.addstr(3, 2, "[5] Promote Sparta (35G)", curses.color_pair(3))
            else:
                stdscr.addstr(3, 2, "RANK UP: Sparta Active!", curses.color_pair(1))
        elif s_type == "G":
            s_display = "Shield Guard (G): 6G"
            stdscr.addstr(3, 2, "RANK UP: Shield Guard Active!", curses.color_pair(1))
        elif s_type == "P":
            s_display = "Paladin (P): 6G"
            if a_type != "&" and k_type != "@":
                stdscr.addstr(3, 2, "[5] Promote Paladin (35G)", curses.color_pair(3))
            else:
                stdscr.addstr(3, 2, "RANK UP: Paladin Active!", curses.color_pair(1))
        else: # "U"
            s_display = "Crusader (U): 6G"
            stdscr.addstr(3, 2, "RANK UP: Crusader Active!", curses.color_pair(1))

        # --- [동적 UI] 2. 궁수 설정 ---
        if a_type == "&":
            a_display = "Archer (&): 5G"
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
            k_display = "Knight (@): 12G"
            # 궁수 전직까지 완료된 후에만 기병 전직 가이드 표시
            if a_type != "&":
                stdscr.addstr(5, 2, "[5] Promote Knight (30G)", curses.color_pair(3))
        elif k_type == "C":
            k_display = "Chariot (C): 15G"
            stdscr.addstr(5, 2, "RANK UP: Chariot Active!", curses.color_pair(1))
        elif k_type == "W": # "W"
            k_display = "W.Hussar (W): 13G"
            stdscr.addstr(5, 2, "RANK UP: W.Hussar Active!", curses.color_pair(1))
        elif k_type == "D":
            k_display = "Dragoon (D): 15G"
            stdscr.addstr(5, 2, "RANK UP: Dragoon Active!", curses.color_pair(1))

        if current_special == "L":
            sp_display = "Fenrir (L): 4G"
        elif current_special == "R":
            sp_display = "Ronin (R): 8G"
        else:
            sp_display = "None (Menu: 4)"

        # 오른쪽 생산 메뉴 출력 (현재 유닛 타입 반영)
        stdscr.addstr(1, 35, f"[1] {s_display}")
        stdscr.addstr(2, 35, f"[2] {a_display}")
        stdscr.addstr(3, 35, f"[3] {k_display}")
        stdscr.addstr(4, 35, f"[4] {sp_display}", curses.color_pair(1) if current_special else curses.color_pair(3))
        
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
            color = curses.color_pair(1) if u.team == "player" else curses.color_pair(2)
            if getattr(u, "shield_hp", 0) > 0:
                try: stdscr.addstr(ground_y - 2, x_pos, "O", color | curses.A_BOLD)
                except: pass
            if u.kind in ["&", "M", "J","F","D"] and u.state_timer > 0:
                char = "$" # 원거리 공격 연출
            
            # 1. 로닌의 발도술에 맞았을 때 (0.2초간 / 표시)
            elif u.state_timer > 0 and u.state_timer <= 0.2:
                char = "/"

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
                stdscr.addstr(start_y + 3, start_x + 3, "[6] Musketeer: DMG 9, Range 6 (8G)", curses.color_pair(1))
                stdscr.addstr(start_y + 4, start_x + 3, "[7] Javelin  : Fast Attack     (6G)", curses.color_pair(1))
                stdscr.addstr(start_y + 5, start_x + 3, "[8] Fire Arc : 10% MaxHP Dmg   (7G)", curses.color_pair(1))
                stdscr.addstr(start_y + 7, start_x + 16, "COST: 25 GOLD", curses.color_pair(2))
            elif show_promo_mode == 3:
                stdscr.addstr(start_y + 1, start_x + 13, "--- KNIGHT PROMOTION ---", curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(start_y + 3, start_x + 3, "[6] Chariot: HP 45, Fast Atk (15G)", curses.color_pair(1))
                stdscr.addstr(start_y + 4, start_x + 3, "[7] W.Hussar: DMG 9, Range 1.5 (13G)", curses.color_pair(1))
                stdscr.addstr(start_y + 5, start_x + 3, "[8] Dragoon: Gun and Sword (15G)", curses.color_pair(1))
                stdscr.addstr(start_y + 7, start_x + 16, "COST: 30 GOLD", curses.color_pair(2))
            elif show_promo_mode == 4:
                stdscr.addstr(start_y + 1, start_x + 13, "--- SPECIAL UNLOCK ---", curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(start_y + 3, start_x + 3, "[6] Fenrir Wolf Warrior: Anti-Archer (4G)", curses.color_pair(3))
                stdscr.addstr(start_y + 4, start_x + 5, "[7] Ronin : Iaijutsu(x2 Dmg) (8G)", curses.color_pair(3))
                stdscr.addstr(start_y + 7, start_x + 16, "COST: 30 GOLD", curses.color_pair(2))
                stdscr.addstr(start_y + 8, start_x + 12, "Press [4] to Close", curses.color_pair(3))
            elif show_promo_mode == 5:
                stdscr.addstr(start_y + 1, start_x + 10, "--- SOLDIER 2ND PROMOTION ---", curses.color_pair(3) | curses.A_BOLD)
                if s_type == "S":
                    stdscr.addstr(start_y + 3, start_x + 3, "[6] Halberd: HP 18, DMG 8 (6G)", curses.color_pair(1))
                    stdscr.addstr(start_y + 4, start_x + 3, "    Anti-cavalry plus max HP damage", curses.color_pair(1))
                elif s_type == "T":
                    stdscr.addstr(start_y + 3, start_x + 3, "[6] Shield Guard: HP 33, DMG 5 (6G)", curses.color_pair(1))
                    stdscr.addstr(start_y + 4, start_x + 3, "    Shield blocks one oversized hit", curses.color_pair(1))
                elif s_type == "P":
                    stdscr.addstr(start_y + 3, start_x + 3, "[6] Crusader: HP 26, DMG 7 (6G)", curses.color_pair(1))
                    stdscr.addstr(start_y + 4, start_x + 3, "    Heals 1 HP every 2 attacks", curses.color_pair(1))
                stdscr.addstr(start_y + 7, start_x + 16, "COST: 35 GOLD", curses.color_pair(2))
        stdscr.refresh()
