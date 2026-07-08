# ai.py
import random
import time

from .unit import Unit

ai_current_types = {"soldier": "#", "archer": "&", "knight": "@"}

def unit_cost(kind):
    return Unit(kind, "ai", 0).cost

def ai_spawn(ai_units, ai_gold, spawn_x, start_time, difficulty="Hard"):
    global ai_current_types
    elapsed = time.time() - start_time

    if difficulty == "Easy":
        cost_mult = 1.3
        time_mult = 1.35
    elif difficulty == "Medium":
        cost_mult = 0.9
        time_mult = 1.15
    else:
        cost_mult = 0.7
        time_mult = 1.0

    # --- [수정] 전직 타이밍 조절 (time_mult 적용) ---
    if elapsed >= (50 * time_mult) and ai_current_types["soldier"] == "#":
        ai_current_types["soldier"] = random.choice(["S", "P", "T"])
    if elapsed >= (100 * time_mult) and ai_current_types["archer"] == "&":
        ai_current_types["archer"] = random.choice(["M", "J", "F"])
    if elapsed >= (140 * time_mult) and ai_current_types["knight"] == "@":
        ai_current_types["knight"] = random.choice(["C", "W", "D"])

    soldier_cost = unit_cost(ai_current_types["soldier"]) * cost_mult
    archer_cost = unit_cost(ai_current_types["archer"]) * cost_mult
    knight_cost = unit_cost(ai_current_types["knight"]) * cost_mult

    if ai_gold < soldier_cost:
        return ai_gold

    if ai_gold >= knight_cost:
        rand = random.random()
        if rand < 0.5:
            ai_units.append(Unit(ai_current_types["knight"], "ai", spawn_x))
            ai_gold -= knight_cost
        elif rand < 0.8 and ai_gold >= archer_cost:
            ai_units.append(Unit(ai_current_types["archer"], "ai", spawn_x))
            ai_gold -= archer_cost
        else:
            ai_units.append(Unit(ai_current_types["soldier"], "ai", spawn_x))
            ai_gold -= soldier_cost
    elif ai_gold >= archer_cost:
        rand = random.random()
        if rand < 0.6:
            ai_units.append(Unit(ai_current_types["archer"], "ai", spawn_x))
            ai_gold -= archer_cost
        else:
            ai_units.append(Unit(ai_current_types["soldier"], "ai", spawn_x))
            ai_gold -= soldier_cost
    else:
        ai_units.append(Unit(ai_current_types["soldier"], "ai", spawn_x))
        ai_gold -= soldier_cost
    return ai_gold
