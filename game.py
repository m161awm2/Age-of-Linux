import time
import curses

from unit import Unit
from economy import Economy
from ai import ai_spawn
from combat import can_attack, try_attack, attack_base
from render import draw

def run(stdscr):
    # ======================
    # 초기 설정
    # ======================
    curses.curs_set(0)
    stdscr.nodelay(True)
    height, width = stdscr.getmaxyx()

    # 화면 기준 좌표    
    GROUND_Y = height - 3
    PLAYER_BASE_X = 2
    AI_BASE_X = width - 3
    # 업그레이드 단계 (0단계부터 시작)
    hp_level = 0
    dmg_level = 0

    # 업그레이드 비용 설정
    hp_upgrade_cost = 15
    dmg_upgrade_cost = 17
    # 게임 데이터
    player_base_hp = 100
    ai_base_hp = 500
    player_units = []
    ai_units = []
    
    # 시스템 객체 (경제)
    eco = Economy()
    ai_eco = Economy()

    last_time = time.time()

    # ======================
    # 메인 루프
    # ======================
    while True:
        # 델타 타임 계산
        now = time.time()
        dt = now - last_time
        last_time = now

        key = stdscr.getch()
        if key == ord('q'): # 종료 키
            break
        # 9번: 체력 업그레이드 로직
        if key == ord("9") and eco.gold >= hp_upgrade_cost:
            eco.gold -= hp_upgrade_cost
            hp_level += 1
            # 다음 업그레이드 비용은 더 비싸지게 (2.5배)
            hp_upgrade_cost = int(hp_upgrade_cost * 2.5)

        # 0번: 공격력 업그레이드 로직
        if key == ord("0") and eco.gold >= dmg_upgrade_cost:
            eco.gold -= dmg_upgrade_cost
            dmg_level += 1
            # 다음 업그레이드 비용은 더 비싸지게 (2.5배)
            dmg_upgrade_cost = int(dmg_upgrade_cost * 2.5)

        # 1. 시스템 업데이트
        eco.update(dt)
        ai_eco.update(dt)
        
        for u in player_units + ai_units:
            u.update(dt) # 쿨다운 및 연출 타이머 감소

# 2. 생산 (플레이어) - 업그레이드 레벨 반영 버전
        if key == ord("1") and eco.gold >= 4:
            # 병사 소환 (hp_level, dmg_level 전달)
            player_units.append(Unit("#", "player", PLAYER_BASE_X + 1, hp_level, dmg_level))
            eco.gold -= 4
            
        elif key == ord("2") and eco.gold >= 6:
            # 궁수 소환 (hp_level, dmg_level 전달)
            player_units.append(Unit("&", "player", PLAYER_BASE_X + 1, hp_level, dmg_level))
            eco.gold -= 6
            
        elif key == ord("3") and eco.gold >= 14:
            # 기병 소환 (hp_level, dmg_level 전달)
            player_units.append(Unit("@", "player", PLAYER_BASE_X + 1, hp_level, dmg_level))
            eco.gold -= 14

        # 3. 생산 (AI)
        if ai_eco.timer >= 0.95:
            ai_eco.gold = ai_spawn(ai_units, ai_eco.gold, AI_BASE_X - 1)

        # 4. 이동 로직 (개별 이동 판정 버전)
        SPEED = 6 * dt
        MARGIN = 0.5 

        # 4. 이동 로직 수정 (사거리 무시하고 접근)
        for i, u in enumerate(player_units):
            # 1. 우리 편 유닛 확인 (겹침 방지용 거리 1.1)
            has_friend_ahead = False
            if i > 0:
                friend_ahead = player_units[i-1]
                if u.x >= friend_ahead.x - 1.1:
                    has_friend_ahead = True
            
            # 2. 적 유닛 확인 (사거리 u.range 대신 고정 거리 1.1 사용)
            # 이제 사거리가 5라도 1.1 거리까지 접근합니다.
            is_enemy_near = ai_units and u.x + 1.1 >= ai_units[0].x
            
            # 3. 적 베이스 확인 (사거리 무시하고 베이스 코앞 1.0까지 접근)
            is_base_near = u.x + 1.0 >= AI_BASE_X - MARGIN
            
            if not (has_friend_ahead or is_enemy_near or is_base_near):
                current_speed = SPEED * 1.8 if u.kind == "@" else SPEED
                u.x += current_speed

        # AI 유닛 이동 (같은 방식으로 수정)
        for i, u in enumerate(ai_units):
            has_friend_ahead = False
            if i > 0:
                friend_ahead = ai_units[i-1]
                if u.x <= friend_ahead.x + 1.1:
                    has_friend_ahead = True
            
            is_enemy_near = player_units and u.x - u.range <= player_units[0].x + 0.2
            is_base_near = u.x - u.range <= PLAYER_BASE_X + MARGIN
            
            if not (has_friend_ahead or is_enemy_near or is_base_near):
                current_speed = SPEED * 1.8 if u.kind == "@" else SPEED
                u.x -= current_speed
        # 5. 전투 시스템 (보정치 0.3 추가로 멈춤과 공격 동기화)
        # Player의 공격
        for p in player_units:
            if not ai_units: break
            if p.kind == "#" or p.kind == "@": 
                if abs(p.x - ai_units[0].x) <= p.range + 0.3:
                    try_attack(p, ai_units[0])
            elif p.kind == "&" :
                for target in ai_units:
                    if abs(p.x - target.x) <= p.range + 0.3:
                        try_attack(p, target)
                        break

        # AI의 공격
        for e in ai_units:
            if not player_units: break
            if e.kind == "#" or e.kind == "@":
                if abs(e.x - player_units[0].x) <= e.range + 0.3:
                    try_attack(e, player_units[0])
            elif e.kind == "&":
                for target in player_units:
                    if abs(e.x - target.x) <= e.range + 0.3:
                        try_attack(e, target)
                        break

        # 6. 베이스 공격 (판정 범위를 더 확실하게 1.5로 상향)
        for u in player_units:
            # 유닛의 현재 위치 + 사거리가 AI 베이스 위치에 거의 도달했는지 체크
            dist_to_base = abs(u.x - AI_BASE_X)
            if dist_to_base <= u.range + 1.5:  # 1.5 보정치로 판정 완화
                ai_base_hp = attack_base(u, AI_BASE_X, ai_base_hp)

        for u in ai_units:
            # AI 유닛 위치와 플레이어 베이스 위치 사이의 거리 체크
            dist_to_base = abs(u.x - PLAYER_BASE_X)
            if dist_to_base <= u.range + 1.5:
                player_base_hp = attack_base(u, PLAYER_BASE_X, player_base_hp)

        # 7. 사망 처리 및 보상 (0.75배 적용)
        for u in player_units:
            if not u.alive(): 
                # 내 유닛이 죽으면 AI는 비용의 100%를 가져감
                ai_eco.gold += u.cost

        for e in ai_units:
            if not e.alive(): 
                # AI 유닛이 죽으면 비용의 50%를 가져감
                # u.cost가 아니라 e.cost(죽은 AI 유닛의 비용)로 써야 함을 주의하세요!
                eco.gold += int(e.cost * 0.5)

        player_units = [u for u in player_units if u.alive()]
        ai_units = [e for e in ai_units if e.alive()]

        # 8. 승패 판정
        if player_base_hp <= 0 or ai_base_hp <= 0:
            msg = "YOU WIN" if ai_base_hp <= 0 else "YOU LOSE"
            stdscr.clear()
            stdscr.addstr(height // 2, width // 2 - len(msg)//2, msg)
            stdscr.refresh()
            time.sleep(3)
            break

        # 9. 렌더링
        draw(
            stdscr, width, height, GROUND_Y,
            player_units, ai_units,
            int(eco.gold), player_base_hp, ai_base_hp,
            hp_level, dmg_level, hp_upgrade_cost, dmg_upgrade_cost
        )


        time.sleep(0.03)
