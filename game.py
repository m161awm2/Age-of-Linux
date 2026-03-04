# game.pytarget.hp
import time
import curses

# game.py 최상단
from ai import ai_spawn, ai_current_types  # ai_current_types를 꼭 추가해야 함
from unit import Unit
from economy import Economy
from ai import ai_spawn
from combat import can_attack, try_attack, attack_base
from render import draw

def run(stdscr, difficulty="Hard"):
    # ======================
    # 초기 설정
    # ======================
    curses.curs_set(0)
    stdscr.nodelay(True)
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK) # 아군
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # 적군
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # UI

    height, width = stdscr.getmaxyx()
    GROUND_Y = height - 3
    PLAYER_BASE_X = 2
    AI_BASE_X = width - 3

    # --- [수정] 통합 업그레이드 변수 ---
    army_level = 0
    upgrade_cost = 25  # 시작 가격 (전직과 동일하게 설정하여 전략성 부여)
    # ------------------------------

    # --- 전직 관련 변수 ---
    soldier_type = "#"
    archer_type = "&"
    knight_type = "@"
    show_promo_mode = 0  # 0:꺼짐, 1:보병메뉴, 2:궁수메뉴
    PROMO_COST_S = 20
    PROMO_COST_A = 25
    PROMO_COST_K = 30

    player_base_hp, ai_base_hp = 100, 500
    player_units, ai_units = [], []
    last_bonus_hp = 500
    
    # --- 기존에 있던 eco = Economy() 부분을 아래와 같이 수정/확인 ---
    # 초기 자금은 10G로 모든 난이도 똑같이 고정!
    eco = Economy()
    eco.gold = 10 
    
    ai_eco = Economy()
    ai_eco.gold = 10
    last_time = time.time()
    game_start_time = time.time()
    last_time = time.time()

    unlocked_units = [] 
    current_special = None

    while True:
        now = time.time()
        dt = now - last_time
        
        last_time = now
    # --- 아래 3줄이 누락되어 골드와 쿨다운이 멈춘 상태입니다 ---
        eco.update(dt)      # 플레이어 골드 생산
        ai_eco.update(dt)   # AI 골드 생산
        for u in player_units + ai_units:
            u.update(dt)    # 유닛 공격 쿨다운 및 애니메이션 업데이트
        # -----------------------------------------------------
        key = stdscr.getch()
        if key == ord('q'): break
        # === [수정] 4번 키 로직 ===
        # 1. 스페셜 유닛 메뉴 및 생산 제어 (4번 키)
        if key == ord('4'):
            # 아무것도 해금 안 된 초기 상태라면 메뉴를 열어줌
            if not unlocked_units:
                show_promo_mode = 4 if show_promo_mode != 4 else 0
            # 메뉴가 열려있을 때 4를 누르면 메뉴를 닫음
            elif show_promo_mode == 4:
                show_promo_mode = 0
            # 메뉴가 닫혀있고, 선택된 유닛(current_special)이 있다면 생산
            else:
                if current_special:
                    cost = 4 if current_special == "L" else 8
                    if eco.gold >= cost:
                        # Unit 생성 시 army_level을 반영하여 업그레이드 데미지 적용
                        player_units.append(Unit(current_special, "player", PLAYER_BASE_X + 1, army_level, army_level))
                        eco.gold -= cost

        # 2. 스페셜 메뉴(mode 4) 내부에서의 해금 및 유닛 선택 (6, 7번 키)
        if show_promo_mode == 4:
            # [6번] 펜리르(L) 해금 또는 선택
            if key == ord('6'):
                if "L" not in unlocked_units:
                    if eco.gold >= 30:
                        eco.gold -= 30
                        unlocked_units.append("L")
                        current_special = "L" # 해금 시 바로 선택
                        show_promo_mode = 0
                else:
                    current_special = "L" # 이미 해금됐다면 4번 생산용으로 지정
                    show_promo_mode = 0
            
            # [7번] 로닌(R) 해금 또는 선택
            elif key == ord('7'):
                if "R" not in unlocked_units:
                    if eco.gold >= 15:
                        eco.gold -= 15
                        unlocked_units.append("R")
                        current_special = "R" # 해금 시 바로 선택
                        show_promo_mode = 0
                else:
                    current_special = "R" # 이미 해금됐다면 4번 생산용으로 지정
                    show_promo_mode = 0
        # =========================

        # 1. 전직 메뉴 제어 (5번 키: 보병 -> 궁수 -> 기병 순서)
        if key == ord("5"):
            if show_promo_mode != 0:
                show_promo_mode = 0
            else:
                if soldier_type == "#": show_promo_mode = 1
                elif archer_type == "&": show_promo_mode = 2
                elif knight_type == "@": show_promo_mode = 3
                else: show_promo_mode = 0

        # 2. 전직 선택 로직 (6번: 1트리, 7번: 2트리)
        if show_promo_mode == 1: # 보병 (25G)
            if key == ord("6") and eco.gold >= 20:
                eco.gold -= 20
                soldier_type = "S"; show_promo_mode = 0
            elif key == ord("7") and eco.gold >= 20:
                eco.gold -= 20
                soldier_type = "P"; show_promo_mode = 0
            elif key == ord("8") and eco.gold >= PROMO_COST_S: # 스파르타 추가
                eco.gold -= PROMO_COST_S
                soldier_type = "T"
                show_promo_mode = 0
        
        elif show_promo_mode == 2: # 궁수 (30G)
            if key == ord("6") and eco.gold >= 25:
                eco.gold -= 25
                archer_type = "M"; show_promo_mode = 0
            elif key == ord("7") and eco.gold >= 25:
                eco.gold -= 25
                archer_type = "J"; show_promo_mode = 0
            elif key == ord("8") and eco.gold >= 25:
                eco.gold -= 25
                archer_type = "F"; show_promo_mode = 0
                
        elif show_promo_mode == 3: # 기병 (50G)
            if key == ord("6") and eco.gold >= 30:
                eco.gold -= 30
                knight_type = "C" # Chariot
                show_promo_mode = 0
            elif key == ord("7") and eco.gold >= 30:
                eco.gold -= 30
                knight_type = "W" # Winged Hussar
                show_promo_mode = 0
            elif key == ord("8") and eco.gold >= 30:
                eco.gold -= 30
                knight_type = "D" #드라군
                show_promo_mode = 0

        # 3. 유닛 생산 (현재 전직 타입 반영)
        # game.py의 입력 처리 부분 수정

        if show_promo_mode == 0:
            # --- 1번: 보병 계열 생산 ---
            if key == ord("1"):
                # 팔라딘(P)과 스파르타(T)는 6원, 나머지는 4원
                cost = 6 if soldier_type in ["P", "T"] else 4
                if eco.gold >= cost:
                    player_units.append(Unit(soldier_type, "player", PLAYER_BASE_X + 1, army_level, army_level))
                    eco.gold -= cost
            
            # --- 2번: 궁수 계열 생산 ---
            elif key == ord("2"):
                # 머스킷(M)은 8원, 투창병(J)과 기본 궁수(&)는 6원
                if archer_type == "M":
                    cost = 8 
                elif archer_type == "J":
                    cost = 6
                elif archer_type == "F":
                    cost = 7    
                else:
                    cost = 5
                if eco.gold >= cost:
                    player_units.append(Unit(archer_type, "player", PLAYER_BASE_X + 1, army_level, army_level))
                    eco.gold -= cost

            # --- 3번: 기병 계열 생산 ---
            elif key == ord("3"):
                # 전차(C)는 20원, 윙드 후사르(W)는 17원, 기본 기사(@)는 14원
                if knight_type == "C":
                    cost = 20
                elif knight_type == "W":
                    cost = 17
                elif knight_type == "D":
                    cost = 18
                else:
                    cost = 14
                
                if eco.gold >= cost:
                    player_units.append(Unit(knight_type, "player", PLAYER_BASE_X + 1, army_level, army_level))
                    eco.gold -= cost
        # [추가] 4. 통합 업그레이드 (9번 키)
        if key == ord("9") and eco.gold >= upgrade_cost:
            eco.gold -= upgrade_cost
            army_level += 1
            upgrade_cost = int(upgrade_cost * 1.6)  # 강화할수록 비용 상승
        # 6. 생산 (AI)
        if ai_eco.timer >= 0.95:
            ai_eco.gold = ai_spawn(ai_units, ai_eco.gold, AI_BASE_X - 1, game_start_time, difficulty)

        # 7. 이동 로직
        SPEED = 6 * dt
        for i, u in enumerate(player_units):
            if not u.alive(): continue
            stop = False
            if i > 0 and u.x >= player_units[i-1].x - 1.1: stop = True
            if ai_units and u.x + 1.1 >= ai_units[0].x: stop = True
            if u.x + 1.0 >= AI_BASE_X - 0.5: stop = True
            if not stop:
                is_cavalry = u.kind in ["@", "C", "W", "D","L"]
                u.x += SPEED * 1.8 if is_cavalry else SPEED

        for i, u in enumerate(ai_units):
            stop = False
    # 1. 앞서가는 자기 팀 유닛이 있으면 멈춤
            if i > 0 and u.x <= ai_units[i-1].x + 1.1: stop = True
    
    # 2. 플레이어 유닛과 일정 거리(1.1) 이하로 가까워지면 멈춤 (u.range 삭제)
            if player_units and u.x <= player_units[0].x + 1.1: stop = True
    
    # 3. 플레이어 베이스 근처에 도달하면 멈춤 (u.range 삭제)
            if u.x <= PLAYER_BASE_X + 1.5: stop = True
    
            if not stop:
                is_cavalry = u.kind in ["@", "C", "W", "D","L"]
                u.x -= SPEED * 1.8 if is_cavalry else SPEED

        # 8. 전투 로직
        for p in player_units:
            if not p.alive(): continue
            if not ai_units: break
            if p.kind in ["#", "@", "S", "P","T", "C", "W","D","L","R"]:
                if abs(p.x - ai_units[0].x) <= p.range + 0.3:
                    try_attack(p, ai_units[0])
            elif p.kind in ["&", "M", "J","F"]:
                for target in ai_units:
                    if abs(p.x - target.x) <= p.range + 0.3:
                        try_attack(p, target)
                        break

        for e in ai_units:
            if not player_units: break
            if e.kind in ["#", "@", "S", "P", "C", "W", "T","D","L"]:
                if abs(e.x - player_units[0].x) <= e.range + 0.3:
                    try_attack(e, player_units[0])
            elif e.kind in ["&", "M", "J","F"]:
                for target in player_units:
                    if abs(e.x - target.x) <= e.range + 0.3:
                        try_attack(e, target)
                        break

        # 9. 베이스 공격 및 사망 처리
        for u in player_units:
            if abs(u.x - AI_BASE_X) <= u.range + 1.5:
                ai_base_hp = attack_base(u, AI_BASE_X, ai_base_hp)
        for u in ai_units:
            if abs(u.x - PLAYER_BASE_X) <= u.range + 1.5:
                player_base_hp = attack_base(u, PLAYER_BASE_X, player_base_hp)
        if last_bonus_hp - ai_base_hp >= 50:
             ai_eco.gold += 20
             last_bonus_hp -= 50  # 다음 50 구간을 위해 업데이트 (예: 100->50, 50->0)

        for u in player_units:
            if not u.alive(): ai_eco.gold += u.cost
        for e in ai_units:
            if not e.alive(): eco.gold += int(e.cost * 0.5)

        player_units = [u for u in player_units if u.alive() or u.state_timer > 0]
        ai_units = [e for e in ai_units if e.alive() or e.state_timer > 0]
        # 10. 승패 판정
        if player_base_hp <= 0 or ai_base_hp <= 0:
            msg = "YOU WIN" if ai_base_hp <= 0 else "YOU LOSE"
            stdscr.clear()
            stdscr.addstr(height // 2, width // 2 - len(msg)//2, msg)
            stdscr.refresh()
            time.sleep(3)
            break

        # 11. [수정] 렌더링 호출 (army_level 전달)
        draw(
            stdscr, width, height, GROUND_Y,
            player_units, ai_units,
            int(eco.gold), player_base_hp, ai_base_hp,
            army_level, army_level, upgrade_cost, upgrade_cost, 
            show_promo_mode, soldier_type, archer_type, knight_type,
            ai_current_types["soldier"],             
            ai_current_types["archer"],              
            ai_current_types["knight"],
            unlocked_units,    # 순서 주의: unlocked_units 다음에
            current_special    # 마지막으로 current_special 전달
        )
        time.sleep(0.03)
