from collections import defaultdict
import time

def score_solution(sol, variables_info):
    """Avalia soft constraints, menor é melhor"""
    penalty = 0
    details = defaultdict(int)

    def day_of_slot(slot):
        return (slot - 1)//4 + 1

    # lições mesmo curso em dias distintos
    for var, meta in variables_info.items():
        c = meta['course']
        v1 = f"{c}_1"
        v2 = f"{c}_2"
        if v1 in sol and v2 in sol and day_of_slot(sol[v1][0]) == day_of_slot(sol[v2][0]):
            penalty += 10
            details['same_course_same_day'] += 1

    # aulas consecutivas, minimizar dias e salas extra
    class_to_slots = defaultdict(list)
    class_to_rooms = defaultdict(set)
    for var, val in sol.items():
        cls = variables_info[var]['class']
        class_to_slots[cls].append(val[0])
        class_to_rooms[cls].add(val[1])

    for cls, slots in class_to_slots.items():
        days = set((s-1)//4+1 for s in slots)
        if len(days) > 4: penalty += 5; details['class_uses_5_days'] += 1
    for cls, rooms in class_to_rooms.items():
        if len(rooms) > 1: penalty += 2*(len(rooms)-1); details['extra_rooms'] += 1

    return penalty, dict(details)


def find_best_solution(problem, variables_info, max_solutions=50, time_limit_seconds=None):
    """
    Itera sobre várias soluções (limitadas) e devolve a melhor pelo score.
    """
    best = None
    best_score = float('inf')
    sols_examined = 0
    start_time = time.time()

    for sol in problem.getSolutionIter():
        score, _ = score_solution(sol, variables_info)
        sols_examined += 1
        if score < best_score:
            best_score = score
            best = sol
        if max_solutions and sols_examined >= max_solutions:
            break
        if time_limit_seconds and (time.time()-start_time) > time_limit_seconds:
            break

    return best, best_score, sols_examined


def print_solution(sol, variables_info):
    if sol is None:
        print("Sem solução")
        return
    days_names = {1:"Seg",2:"Ter",3:"Qua",4:"Qui",5:"Sex"}
    schedule = defaultdict(lambda: defaultdict(list))
    for var, val in sol.items():
        slot, room = val
        cls = variables_info[var]['class']
        course = variables_info[var]['course']
        pos = (slot-1)%4+1
        day = (slot-1)//4+1
        schedule[cls][day].append((pos, course, room))
    for cls in sorted(schedule.keys()):
        print(f"=== Classe {cls} ===")
        for d in range(1,6):
            entries = sorted(schedule[cls].get(d,[]))
            if entries:
                print(f" {days_names[d]}: ", ", ".join(f"bloco{pos} {course} ({room})" for pos,course,room in entries))
        print()
