def distance(a, b):
    return abs(a.x - b.x)

def can_attack(attacker, target, allies, enemies):
    dist = abs(attacker.x - target.x)

    # 근접 병사 (#)
    if attacker.kind == "#":
        # 적 리스트가 비어있지 않고, 타겟이 가장 앞의 적이며, 사거리 이내일 때
        return len(enemies) > 0 and target == enemies[0] and dist <= attacker.range

    # 궁수 (&)
    elif attacker.kind == "&":
        # 사거리 이내라면 누구든 공격 가능
        return dist <= attacker.range

    return False

def try_attack(attacker, target):
    # 쿨다운이 다 찼을 때만 공격 실행
    if attacker.cooldown <= 0:
        target.hp -= attacker.damage
        attacker.cooldown = attacker.attack_speed
        
        # 🏹 🌟 추가: 궁수(&)가 공격할 때 0.2초간 $로 변신하도록 타이머 설정
        # combat.py 의 try_attack 함수 내부
        if attacker.kind in ["&", "M", "J"]:
            attacker.state_timer = 0.2

def attack_base(unit, base_x, base_hp):
    # 🌟 여기서 거리 체크(if abs...)를 하고 있다면 지워버리세요!
    if unit.cooldown <= 0:
        base_hp -= unit.damage
        unit.cooldown = unit.attack_speed
        
        # 궁수라면 $ 연출 타이머 작동
        if unit.kind == "&":
            unit.state_timer = 0.2
            
    return base_hp