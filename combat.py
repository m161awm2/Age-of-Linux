# combat.py

def distance(a, b):
    return abs(a.x - b.x)

def can_attack(attacker, target, allies, enemies):
    dist = abs(attacker.x - target.x)

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
        # --- [추가] 상성 로직: 창병(S)이 기병(@, C, W)을 공격할 때 1.5배 데미지 ---
        actual_damage = attacker.damage
        
        if attacker.kind == "S" and target.kind in ["@", "C", "W"]:
            actual_damage = int(attacker.damage * 1.5)
        
        target.hp -= actual_damage
        # ------------------------------------------------------------------

        attacker.cooldown = attacker.attack_speed
        
        # 🏹 궁수 계열 변신 연출 타이머
        if attacker.kind in ["&", "M", "J"]:
            attacker.state_timer = 0.2

def attack_base(unit, base_x, base_hp):
    if unit.cooldown <= 0:
        base_hp -= unit.damage
        unit.cooldown = unit.attack_speed
        
        if unit.kind == "&":
            unit.state_timer = 0.2
            
    return base_hp