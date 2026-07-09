# combat.py

def distance(a, b):
    return abs(a.x - b.x)

CAVALRY_KINDS = {"@", "C", "W", "D"}

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
    """
    실제 공격 로직을 처리합니다. (들여쓰기 및 변수명 수정 완료)
    """
    # 1. 쿨다운이 다 찼을 때만 공격 실행
    if attacker.cooldown <= 0:
        dist = abs(attacker.x - target.x)
        
        # 2. 기본 데미지 설정 (unit.py의 self.damage 참조)
        actual_damage = attacker.damage

        if attacker.kind in ["W", "Y"]:
            actual_damage = round(actual_damage * attacker.charge_damage_multiplier())
        
        # 3. [드라군 전용 로직] 거리에 따라 공격 방식 변경
        is_melee_attack = False
        if attacker.kind == "D":
            if dist <= 1.5:  # 근접 상황 (칼)
                actual_damage = int(attacker.damage * 1.5)
                attacker.cooldown = 1.0
                is_melee_attack = True
            else:           # 원거리 상황 (총)
                attacker.cooldown = 2.0
                is_melee_attack = False

        # 4. [펜리르(L) 상성 시스템]
        ranged_list = ["&", "M", "J", "F", "D"]
        
        # (1) 펜리르가 원거리 유닛 공격 시: 데미지 40% 증가
        if attacker.kind == "L" and target.kind in ranged_list:
            actual_damage = int(actual_damage * 1.4)
            
        # (2) 원거리 유닛이 펜리르 공격 시: 데미지 40% 감소 (근접 드라군 제외)
        if attacker.kind in ranged_list and target.kind == "L":
            is_dragoon_melee = (attacker.kind == "D" and dist <= 1.5)
            if not is_dragoon_melee:
                actual_damage = int(actual_damage * 0.6)

        # 광폭화 중인 바이킹 광전사는 1대1 교전에 특화됩니다.
        if attacker.kind == "V" and attacker.is_berserking():
            actual_damage = int(actual_damage * 2.0)

        # 5. [기타 상성 로직]
        # 창병 계열이 기병(@, C, W, D)을 공격할 때 추가 데미지
        if attacker.kind in ["S", "H"] and target.kind in ["@", "C", "W", "D"]:
            actual_damage = int(actual_damage * 1.8)

        # 할버드병은 모든 병사에게 최대 체력 비례 피해를 추가로 줍니다.
        if attacker.kind == "H":
            actual_damage += int(target.max_hp * 0.12)
            
        # 6. [불화살 사수(F) 로직] 적 최대 체력 비례 데미지
        if attacker.kind == "F":
            actual_damage += int(target.max_hp * 0.12)

        # 7. [로닌(R) 발도술] 첫 공격 2배 데미지
        if attacker.kind == "R" and getattr(attacker, 'is_first_strike', False):
            actual_damage = int(actual_damage * 2.0)
            attacker.is_first_strike = False 
            target.state_timer = 0.2 # 피격 연출

        # 8. 최종 데미지 적용 및 체력 차감
        if target.kind == "V" and target.is_berserking():
            actual_damage = max(1, int(actual_damage * 0.4))
        parried = False
        if target.kind == "Y" and target.can_parry():
            target.use_parry()
            attacker.take_damage(actual_damage * 2)
            attacker.parry_hit_timer = 0.2
            parried = True
        if not parried:
            target.take_damage(actual_damage)
            if attacker.kind == "V":
                attacker.heal(1)
        if attacker.kind == "U" and not parried:
            attacker.heal_counter = getattr(attacker, "heal_counter", 0) + 1
            if attacker.heal_counter >= 2:
                attacker.heal(1)
                attacker.heal_counter = 0
        attacker.reset_charge()

        is_dragoon_ranged = attacker.kind == "D" and dist > 1.5

        # 창병은 기병별 첫 돌격을 받아낼 때 한 번만 반격 피해를 줍니다.
        if (
            target.kind in ["S", "H"]
            and attacker.kind in CAVALRY_KINDS
            and not is_dragoon_ranged
            and not getattr(attacker, "took_spearman_counter", False)
        ):
            attacker.hp -= target.damage
            attacker.took_spearman_counter = True

        # 9. [후처리] 쿨다운 및 연출 설정
        if attacker.kind != "D":
            attacker.cooldown = attacker.attack_speed * 0.6 if attacker.is_berserking() else attacker.attack_speed
        
        # 원거리 공격자 연출 타이머
        if attacker.kind in ["&", "M", "J", "F"]:
            attacker.state_timer = 0.2
        elif attacker.kind == "D" and not is_melee_attack:
            attacker.state_timer = 0.2
def attack_base(unit, base_x, base_hp):
    if unit.cooldown <= 0:
        actual_damage = unit.damage
        if unit.kind == "V" and unit.is_berserking():
            actual_damage = int(actual_damage * 2.0)
        base_hp -= actual_damage
        unit.reset_charge()
        unit.cooldown = unit.attack_speed * 0.6 if unit.is_berserking() else unit.attack_speed
        
        if unit.kind == "&":
            unit.state_timer = 0.2
            
    return base_hp
