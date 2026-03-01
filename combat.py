# combat.py

def distance(a, b):
    return abs(a.x - b.x)

def can_attack(attacker, target, allies, enemies):
    dist = abs(attacker.x - target.x)
    if attacker.kind == "D":
        return dist <= attacker.range
    # 근접 병사 (#)
    if attacker.kind == "#":
        return len(enemies) > 0 and target == enemies[0] and dist <= attacker.range

    # 궁수 (&)
    elif attacker.kind == "&":
        return dist <= attacker.range

    return False

# combat.py

def try_attack(attacker, target):
    # 쿨다운이 다 찼을 때만 공격 실행
    if attacker.cooldown <= 0:
        dist = abs(attacker.x - target.x)
        
        # 1. [기본 데미지 설정] 먼저 기본 데미지를 가져옵니다.
        actual_damage = attacker.damage
        
        # 2. [드라군 전용 로직] 드라군은 상황에 따라 데미지와 쿨다운이 변함
        is_melee_attack = False
        if attacker.kind == "D":
            if dist <= 1.5:  # 근접 상황 (칼)
                actual_damage = int(attacker.damage * 1.5)
                attacker.cooldown = 1.0
                is_melee_attack = True
            else:           # 원거리 상황 (총)
                actual_damage = attacker.damage
                attacker.cooldown = 2.0
                is_melee_attack = False

        # 3. === [추가] 펜리르(L) 상성 시스템 ===
        ranged_list = ["&", "M", "J", "F", "D"]
        
        # (1) 펜리르(L)가 원거리 유닛 공격 시: 데미지 30% 증가
        if attacker.kind == "L" and target.kind in ranged_list:
            actual_damage = int(actual_damage * 1.4)
            
        # (2) 원거리 유닛이 펜리르(L) 공격 시: 데미지 30% 감소 (단, 드라군 근접 제외)
        if attacker.kind in ranged_list and target.kind == "L":
            is_dragoon_melee = (attacker.kind == "D" and dist <= 1.5)
            if not is_dragoon_melee:
                actual_damage = int(actual_damage * 0.6)
        # ======================================

        # 4. [기타 상성 로직]
        # 창병(S)이 기병(@, C, W, D)을 공격할 때 1.5배 데미지
        if attacker.kind == "S" and target.kind in ["@", "C", "W", "D"]:
            actual_damage = int(actual_damage * 1.5)
            
        # 불화살 사수(F)의 고정 퍼센트 데미지
        if attacker.kind == "F":
            bonus_ratio = 0.10 + (attacker.dmg_lv * 0.03)
            actual_damage += int(target.max_hp * bonus_ratio)
        # 5. [최종 데미지 적용]
        target.hp -= actual_damage

        # 6. [후처리] 쿨다운 및 연출 설정
        if attacker.kind != "D":
            attacker.cooldown = attacker.attack_speed
        
        if attacker.kind in ["&", "M", "J", "F"]:
            attacker.state_timer = 0.2
        elif attacker.kind == "D" and not is_melee_attack:
            attacker.state_timer = 0.2
        # 로닌 발도술
        if attacker.kind == "R" and attacker.is_first_strike:
            actual_damage = int(actual_damage * 2.0) # 첫 공격 2배 데미지
            attacker.is_first_strike = False 
            
            # [추가] 피격된 적 유닛에게 0.2초간 베이는 연출 부여
            # target의 state_timer를 0.2로 설정하여 render.py에서 '/'로 그리게 함
            target.state_timer = 0.2
def attack_base(unit, base_x, base_hp):
    if unit.cooldown <= 0:
        base_hp -= unit.damage
        unit.cooldown = unit.attack_speed
        
        if unit.kind == "&":
            unit.state_timer = 0.2
            
    return base_hp
