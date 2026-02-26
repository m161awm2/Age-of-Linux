# unit.py

class Unit:
    # 🌟 hp_lv과 dmg_lv을 인자로 받도록 수정 (기본값 0)
    def __init__(self, kind, team, x, hp_lv=0, dmg_lv=0):
        self.kind = kind
        self.team = team
        self.x = x
        self.state_timer = 0
        self.cooldown = 0

        # 유닛 종류별 스탯 설정
        if kind == "#": # 보병
            # 🌟 레벨당 체력 +2, 공격력 +2 적용
            self.max_hp = 15 + (hp_lv * 2)
            self.damage = 5 + (dmg_lv * 2)
            self.cost = 4
            self.range = 1
            self.attack_speed = 1.0
            
        elif kind == "&": # 궁수
            # 🌟 레벨당 체력 +2, 공격력 +2 적용
            self.max_hp = 9 + (hp_lv * 2)
            self.damage = 3 + (dmg_lv * 2)
            self.cost = 6
            self.range = 5
            self.attack_speed = 1.2
            
        elif kind == "@": # 기병
            # 🌟 기병은 비싸니까 레벨당 체력 +4, 공격력 +4 적용 (보너스!)
            self.max_hp = 27 + (hp_lv * 3)
            self.damage = 9 + (dmg_lv * 4)
            self.cost = 14
            self.range = 2
            self.attack_speed = 1.5

        # 현재 체력을 계산된 최대 체력으로 설정
        self.hp = self.max_hp

    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt
        if self.state_timer > 0: # 👈 이 줄도 확인!
            self.state_timer -= dt

    def alive(self):

        return self.hp > 0
