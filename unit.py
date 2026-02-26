# unit.py
import math

class Unit:
    def __init__(self, kind, team, x, hp_lv=0, dmg_lv=0):
        self.kind = kind
        self.team = team
        self.x = x
        self.state_timer = 0
        self.cooldown = 0

        # --- 유닛별 기본 스탯 설정 (이 부분이 누락되어 에러가 났습니다) ---
        if kind == "#": # 기본 보병
            base_hp, base_dmg = 15, 5
            self.cost, self.range, self.attack_speed = 4, 1, 1.0
        elif kind == "S": # 창병 (전직)
            base_hp, base_dmg = 15, 7
            self.cost, self.range, self.attack_speed = 4, 2, 1.5
        elif kind == "P": # 팔라딘 (전직)
            base_hp, base_dmg = 25, 6
            self.cost, self.range, self.attack_speed = 6, 1, 0.8
        elif kind == "&": # 기본 궁수
            base_hp, base_dmg = 9, 3
            self.cost, self.range, self.attack_speed = 6, 4, 1.4
        elif kind == "M": # 머스킷병 (전직)
            base_hp, base_dmg = 12, 10
            self.cost, self.range, self.attack_speed = 8, 6, 2.0
        elif kind == "J": # 투창병 (전직)
            base_hp, base_dmg = 15, 5
            self.cost, self.range, self.attack_speed = 6, 3, 1.5
        elif kind == "@": # 기병
            base_hp, base_dmg = 27, 9
            self.cost, self.range, self.attack_speed = 14, 2, 1.2
        elif kind == "C": # Chariot (전직 기병 1)
            base_hp, base_dmg = 60, 1 # 높은 체력, 낮은 단발 데미지
            self.cost, self.range, self.attack_speed = 20, 1, 0.1 # 012초당 공격
        elif kind == "W": # Winged Hussar (전직 기병 2)
            base_hp, base_dmg = 27, 15 # 높은 데미지
            self.cost, self.range, self.attack_speed = 20, 3, 1.2 # 긴 사거리
        else:
            # 혹시 모를 예외 처리
            base_hp, base_dmg = 10, 1
            self.cost, self.range, self.attack_speed = 1, 1, 1.0

        # 업그레이드 복리 계산
        self.max_hp = round(base_hp * math.pow(1.2, hp_lv))
        self.damage = round(base_dmg * math.pow(1.2, dmg_lv))
        self.hp = self.max_hp

    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt
        if self.state_timer > 0:
            self.state_timer -= dt

    def alive(self):

        return self.hp > 0

