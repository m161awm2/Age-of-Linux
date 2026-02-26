# ai.py
import random
from unit import Unit

def ai_spawn(ai_units, ai_gold, spawn_x):
    # 유닛 비용 설정 (사용자가 낮춘 비용 반영 + 기병 추가)
    SOLDIER_COST = 3
    ARCHER_COST = 5
    KNIGHT_COST = 10  # 기병은 강력하니까 10원 정도로 설정해볼까요?

    # 가장 싼 병사조차 못 뽑으면 바로 리턴
    if ai_gold < SOLDIER_COST:
        return ai_gold

    # 1. 돈이 아주 많을 때 (기병 소환 고려)
    if ai_gold >= KNIGHT_COST:
        rand = random.random()
        if rand < 0.5:     # 50% 확률로 기병 소환 (강력한 압박)
            ai_units.append(Unit("@", "ai", spawn_x))
            ai_gold -= KNIGHT_COST
        elif rand < 0.8:   # 30% 확률로 궁수 소환
            ai_units.append(Unit("&", "ai", spawn_x))
            ai_gold -= ARCHER_COST
        else:              # 20% 확률로 병사 소환
            ai_units.append(Unit("#", "ai", spawn_x))
            ai_gold -= SOLDIER_COST

    # 2. 기병은 못 뽑지만 궁수는 뽑을 수 있을 때
    elif ai_gold >= ARCHER_COST:
        if random.random() < 0.4: # 40% 확률로 궁수 소환
            ai_units.append(Unit("&", "ai", spawn_x))
            ai_gold -= ARCHER_COST
        else:                     # 나머지 확률로 병사를 뽑거나 돈을 더 모음
            if random.random() < 0.5:
                ai_units.append(Unit("#", "ai", spawn_x))
                ai_gold -= SOLDIER_COST

    # 3. 병사만 뽑을 수 있을 때
    elif ai_gold >= SOLDIER_COST:
        # 돈을 아껴서 기병/궁수를 뽑을 수 있게 소환 확률을 낮춤 (전략적 대기)
        if random.random() < 0.2: 
            ai_units.append(Unit("#", "ai", spawn_x))
            ai_gold -= SOLDIER_COST
        
    return ai_gold