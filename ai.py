# ai.py
import random
import time
from unit import Unit

ai_current_types = {"soldier": "#", "archer": "&", "knight": "@"}

def ai_spawn(ai_units, ai_gold, spawn_x, start_time, difficulty="Hard"):
    global ai_current_types
    elapsed = time.time() - start_time
    
    # --- [추가] 난이도별 배수 설정 ---
    if difficulty == "Easy":
        cost_mult = 1.8  # 적 유닛 가격 3배 (보병 12G)
        time_mult = 1.5  # 진급 속도 3배 느림 (150초 뒤 진급)
    elif difficulty == "Medium":
        cost_mult = 1.3  # 적 유닛 가격 1.5배 (보병 6G)
        time_mult = 1.2  # 진급 속도 1.5배 느림 (75초 뒤 진급)
    else: # Hard
        cost_mult = 1.0
        time_mult = 1.0

    # --- [수정] 전직 타이밍 조절 (time_mult 적용) ---
    if elapsed >= (50 * time_mult) and ai_current_types["soldier"] == "#":
        ai_current_types["soldier"] = random.choice(["S", "P", "T"])
    if elapsed >= (100 * time_mult) and ai_current_types["archer"] == "&":
        ai_current_types["archer"] = random.choice(["M", "J", "F"])
    if elapsed >= (140 * time_mult) and ai_current_types["knight"] == "@":
        ai_current_types["knight"] = random.choice(["C", "W", "D"])

    # --- [수정] 난이도가 반영된 적 생산 비용 ---
    SOLDIER_COST = 4 * cost_mult
    ARCHER_COST = 6 * cost_mult
    KNIGHT_COST = 8 * cost_mult

    if ai_gold < SOLDIER_COST:
        return ai_gold

    # --- 생산 알고리즘 (변경된 COST 변수 사용) ---
    if ai_gold >= KNIGHT_COST:
        rand = random.random()
        if rand < 0.5:
            ai_units.append(Unit(ai_current_types["knight"], "ai", spawn_x, 0, 0))
            ai_gold -= KNIGHT_COST
        elif rand < 0.8:
            ai_units.append(Unit(ai_current_types["archer"], "ai", spawn_x, 0, 0))
            ai_gold -= ARCHER_COST
        else:
            ai_units.append(Unit(ai_current_types["soldier"], "ai", spawn_x, 0, 0))
            ai_gold -= SOLDIER_COST
    # ... (생략된 ARCHER_COST 체크 부분도 동일하게 변수 사용)
    return ai_gold
