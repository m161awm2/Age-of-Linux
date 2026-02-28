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

def try_attack(attacker, target):
    # 쿨다운이 다 찼을 때만 공격 실행
    if attacker.cooldown <= 0:
        dist = abs(attacker.x - target.x)
        
        # 드라군(D) 하이브리드 로직
        is_melee_attack = False
        if attacker.kind == "D":
            if dist <= 1.5:  # 1. 근접 상황 (칼)
                actual_damage = int(attacker.damage * 1.5)
                attacker.cooldown = 1.0  # 공속 빨라짐
                is_melee_attack = True   # 모션 없음을 위해 체크
            else:           # 2. 원거리 상황 (총)
                actual_damage = attacker.damage
                attacker.cooldown = 2.0  # 공속 느려짐
                is_melee_attack = False
        # --- [추가] 상성 로직: 창병(S)이 기병(@, C, W)을 공격할 때 1.5배 데미지 ---
        actual_damage = attacker.damage
        
        if attacker.kind == "S" and target.kind in ["@", "C", "W","D"]:
            actual_damage = int(attacker.damage * 1.5)
        if attacker.kind == "F":
            actual_damage += int(target.max_hp * 0.10)
        target.hp -= actual_damage
        # ------------------------------------------------------------------
# 드라군이 아닐 때만 유닛의 기본 공속 적용
        if attacker.kind != "D":
            attacker.cooldown = attacker.attack_speed
        
        # 🏹 궁수 계열 변신 연출 타이머
        if attacker.kind in ["&", "M", "J","F"]:
            attacker.state_timer = 0.2
        elif attacker.kind == "D" and not is_melee_attack:
            attacker.state_timer = 0.2

def attack_base(unit, base_x, base_hp):
    if unit.cooldown <= 0:
        base_hp -= unit.damage
        unit.cooldown = unit.attack_speed
        
        if unit.kind == "&":
            unit.state_timer = 0.2
            
    return base_hp
