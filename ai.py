# ai.py
import random
import time
from unit import Unit

# AI의 현재 유닛 타입을 관리하는 변수 (전역)
ai_current_types = {
    "soldier": "#",
    "archer": "&",
    "knight": "@"
}

def ai_spawn(ai_units, ai_gold, spawn_x, start_time):
    global ai_current_types
    elapsed = time.time() - start_time
    
    # --- 1분마다 랜덤 전직 ---
    if elapsed >= 50 and ai_current_types["soldier"] == "#":
        ai_current_types["soldier"] = random.choice(["S", "P", "T"])
    if elapsed >= 100 and ai_current_types["archer"] == "&":
        ai_current_types["archer"] = random.choice(["M", "J", "F"])
    if elapsed >= 140 and ai_current_types["knight"] == "@":
        ai_current_types["knight"] = random.choice(["C", "W", "D"])

    # 사용자 지정 가격 설정
    SOLDIER_COST = 4
    ARCHER_COST = 6
    KNIGHT_COST = 8

    if ai_gold < SOLDIER_COST:
        return ai_gold

    # --- 사용자 제공 알고리즘 기반 생산 (레벨은 항상 0) ---
    if ai_gold >= KNIGHT_COST:
        rand = random.random()
        if rand < 0.5:
            ai_units.append(Unit(ai_current_types["knight"], "ai", spawn_x, 0, 0)) # 레벨 0
            ai_gold -= KNIGHT_COST
        elif rand < 0.8:
            ai_units.append(Unit(ai_current_types["archer"], "ai", spawn_x, 0, 0)) # 레벨 0
            ai_gold -= ARCHER_COST
        else:
            ai_units.append(Unit(ai_current_types["soldier"], "ai", spawn_x, 0, 0)) # 레벨 0
            ai_gold -= SOLDIER_COST

    elif ai_gold >= ARCHER_COST:
        if random.random() < 0.4: 
            ai_units.append(Unit(ai_current_types["archer"], "ai", spawn_x, 0, 0))
            ai_gold -= ARCHER_COST
        else:
            if random.random() < 0.5:
                ai_units.append(Unit(ai_current_types["soldier"], "ai", spawn_x, 0, 0))
                ai_gold -= SOLDIER_COST

    elif ai_gold >= SOLDIER_COST:
        if random.random() < 0.2: 
            ai_units.append(Unit(ai_current_types["soldier"], "ai", spawn_x, 0, 0))
            ai_gold -= SOLDIER_COST

    return ai_gold