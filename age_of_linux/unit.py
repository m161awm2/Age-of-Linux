CAVALRY_KINDS = {"@", "C", "W", "D"}
ATTACK_WINDUP_RATIO = 0.2
SHIELD_GUARD_SHIELD_HP = 8
WINGED_HUSSAR_CHARGE_STEP = 0.08
WINGED_HUSSAR_MAX_SPEED = 2.4
WINGED_HUSSAR_MAX_DAMAGE_BONUS = 0.2
WINGED_HUSSAR_CHARGE_GRACE = 1.0

class Unit:
    def __init__(self, kind, team, x):
        self.kind = kind
        self.team = team
        self.x = x
        self.state_timer = 0

        # --- 유닛별 기본 스탯 설정 (이 부분이 누락되어 에러가 났습니다) ---
        if kind == "#": # 기본 보병
            base_hp, base_dmg = 15, 5
            self.cost, self.range, self.attack_speed = 4, 1, 1.0
        elif kind == "S": # 창병 (전직)
            base_hp, base_dmg = 16, 7
            self.cost, self.range, self.attack_speed = 4, 2, 1.1
        elif kind == "H": # 할버드 (창병 2차 전직)
            base_hp, base_dmg = 18, 8
            self.cost, self.range, self.attack_speed = 6, 2, 1.0
        elif kind == "P": # 팔라딘 (전직)
            base_hp, base_dmg = 25, 6
            self.cost, self.range, self.attack_speed = 6, 1, 0.7
        elif kind == "U": # 크루세이더 (팔라딘 2차 전직)
            base_hp, base_dmg = 26, 7
            self.cost, self.range, self.attack_speed = 6, 1, 0.7
        elif kind == "T": # 스파르타 (새로운 전직)
            base_hp, base_dmg = 33, 5 
            self.cost, self.range, self.attack_speed = 6, 1, 1.0
        elif kind == "G": # 방패병 (스파르타 2차 전직)
            base_hp, base_dmg = 33, 5
            self.cost, self.range, self.attack_speed = 6, 1, 1.0

        elif kind == "&": # 기본 궁수
            base_hp, base_dmg = 9, 3
            self.cost, self.range, self.attack_speed = 5, 4, 1.4
        elif kind == "M": # 머스킷병 (전직)
            base_hp, base_dmg = 10, 9
            self.cost, self.range, self.attack_speed = 8, 6, 2.0
        elif kind == "J": # 투창병 (전직)
            base_hp, base_dmg = 17, 7
            self.cost, self.range, self.attack_speed = 6, 3, 1.5
        elif kind == "F": # 불화살 사수 (NEW)
            base_hp, base_dmg = 11, 6 
            self.cost, self.range, self.attack_speed = 7, 5, 2.0
            
        elif kind == "@": # 기병
            base_hp, base_dmg = 27, 8
            self.cost, self.range, self.attack_speed = 13, 2, 1.2
        elif kind == "C": # Chariot (전직 기병 1)
            base_hp, base_dmg = 45, 1 # 높은 체력, 낮은 단발 데미지
            self.cost, self.range, self.attack_speed = 15, 1, 0.15
        elif kind == "W": # Winged Hussar (전직 기병 2)
            base_hp, base_dmg = 27, 9 # 돌격 가속을 고려해 단발 데미지 조정
            self.cost, self.range, self.attack_speed = 13, 1.5, 1.2 # 긴 사거리
        elif kind == "D": # 드라군 (사격 기병)
            base_hp, base_dmg = 25, 8 # 기본 데미지는 총 기준
            self.cost, self.range, self.attack_speed = 15, 6, 2.0
        
        elif kind == "L": # 펜리르 늑대전사 (해금 유닛)
            base_hp, base_dmg = 12, 4
            self.cost, self.range, self.attack_speed = 4, 1, 0.5
        elif kind == "R": # 로닌 (Ronin)
            base_hp, base_dmg = 22, 10
            self.cost, self.range, self.attack_speed = 8, 1, 1.0
            # 발도술
            self.is_first_strike = True

        else:
            # 혹시 모를 예외 처리
            base_hp, base_dmg = 10, 1
            self.cost, self.range, self.attack_speed = 1, 1, 1.0

        self.max_hp = base_hp
        self.damage = base_dmg
        self.hp = self.max_hp
        self.max_shield = SHIELD_GUARD_SHIELD_HP if self.kind == "G" else 0
        self.shield_hp = self.max_shield
        self.is_cavalry = self.kind in CAVALRY_KINDS
        self.in_attack_range = False
        self.cooldown = 0 if self.is_cavalry else self.attack_speed * ATTACK_WINDUP_RATIO
        self.charge_tiles = 0
        self.last_charge_tile = int(self.x)
        self.charge_grace_timer = 0

    def update(self, dt):
        if self.cooldown > 0 and (self.is_cavalry or self.in_attack_range):
            self.cooldown -= dt
            if self.cooldown <= 0.001:
                self.cooldown = 0
        if self.kind == "W" and self.charge_grace_timer > 0:
            self.charge_grace_timer -= dt
            if self.charge_grace_timer <= 0:
                self.charge_grace_timer = 0
                self.charge_tiles = 0
                self.last_charge_tile = int(self.x)
        self.in_attack_range = False
        if self.state_timer > 0:
            self.state_timer -= dt

    def alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        if self.shield_hp > 0:
            self.shield_hp -= amount
            if self.shield_hp < 0:
                self.shield_hp = 0
            return
        self.hp -= amount

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def movement_speed_multiplier(self):
        if self.kind == "W":
            return min(
                1.0 + self.charge_tiles * WINGED_HUSSAR_CHARGE_STEP,
                WINGED_HUSSAR_MAX_SPEED,
            )
        if self.kind in CAVALRY_KINDS or self.kind == "L":
            return 1.8
        return 1.0

    def update_charge_after_move(self):
        if self.kind != "W":
            return
        self.charge_grace_timer = 0
        current_tile = int(self.x)
        crossed_tiles = abs(current_tile - self.last_charge_tile)
        if crossed_tiles > 0:
            self.charge_tiles += crossed_tiles
            self.last_charge_tile = current_tile

    def reset_charge(self):
        if self.kind == "W" and self.charge_tiles > 0 and self.charge_grace_timer <= 0:
            self.charge_grace_timer = WINGED_HUSSAR_CHARGE_GRACE

    def charge_damage_multiplier(self):
        if self.kind != "W":
            return 1.0
        speed_gain = self.movement_speed_multiplier() - 1.0
        max_speed_gain = WINGED_HUSSAR_MAX_SPEED - 1.0
        if max_speed_gain <= 0:
            return 1.0
        charge_ratio = min(speed_gain / max_speed_gain, 1.0)
        return 1.0 + WINGED_HUSSAR_MAX_DAMAGE_BONUS * charge_ratio
