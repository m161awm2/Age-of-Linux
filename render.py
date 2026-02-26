def draw(stdscr, width, height, ground_y, p_units, e_units, gold, p_hp, e_hp, hp_lv, dmg_lv, hp_cost, dmg_cost):
    # 1. 화면 초기화 (함수 시작할 때 딱 한 번만!)
    stdscr.clear()

    # 2. 상단 UI (골드, 기지 체력, 업그레이드 정보)
    # 💰, 🏰 같은 이모지는 리눅스 터미널 폰트에 따라 안 보일 수 있으니 텍스트 위주로 구성했습니다.
    stdscr.addstr(0, 2, f"GOLD: {gold}G  |  BASE: {p_hp} vs {e_hp}")
    stdscr.addstr(1, 2, f"[9] HP  Lv.{hp_lv} ({hp_cost}G)")
    stdscr.addstr(2, 2, f"[0] DMG Lv.{dmg_lv} ({dmg_cost}G)")
    stdscr.addstr(1, 30, f"[1] Soldier (#): 4G")
    stdscr.addstr(2, 30, f"[2] Archer  (&): 6G")
    stdscr.addstr(3, 30, f"[3] Knight  (@): 14G")
    # AI 기지 체력 표시 (오른쪽 끝)
    stdscr.addstr(0, width - 15, f"AI BASE: {e_hp}")

    # 3. 바닥 (Ground)
    for x in range(width - 1):
        try:
            stdscr.addstr(ground_y, x, "-")
        except: pass # 화면 끝 예외 처리

    # 4. 베이스 위치 표시
    stdscr.addstr(ground_y - 1, 2, "P")
    stdscr.addstr(ground_y - 1, width - 3, "A")

    # 5. 유닛 그리기
    for u in p_units + e_units:
        # 화면 좌표 제한 (x좌표가 소수점일 수 있으니 int로 변환)
        x_pos = max(0, min(width - 2, int(u.x)))
        
        # 유닛 모양 결정 (궁수가 공격 중이면 $로 변신)
        char = u.kind
        if u.kind == "&" and u.state_timer > 0:
            char = "$"
            
        try:
            stdscr.addstr(ground_y - 1, x_pos, char)
        except: pass

    # 6. 화면 갱신
    stdscr.refresh()