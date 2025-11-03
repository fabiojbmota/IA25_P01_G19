from constraint import Problem
from collections import defaultdict, Counter
import itertools
import random

SLOTS = list(range(1, 21))  # 5 dias * 4 blocos

def day_of_slot(slot):
    return (slot - 1)//4 + 1  # 1..5

def build_problem(data, rooms=None, lessons_per_course=2):
    "Cria o problema CSP com restrições hard simplificadas para dataset"
    if rooms is None:
        rooms = ["Lab01", "RoomA", "RoomB", "RoomC", "RoomD"]

    problem = Problem()
    cc = data['cc']
    course_to_class = {c: cls for cls, courses in cc.items() for c in courses}
    course_list = sorted(course_to_class.keys())
    course_to_teacher = data.get('dsd', {})
    room_restrictions = data.get('rr', {})
    online_info = data.get('oc', {})

    variables_info = {}

    # criar variáveis
    for c in course_list:
        for i in range(1, lessons_per_course+1):
            var = f"{c}_{i}"
            if c in room_restrictions:
                fixed_room = room_restrictions[c]
                domain = [(s, fixed_room) for s in SLOTS]
            else:
                domain = [(s, r) for s in SLOTS for r in rooms]
            # limitar domínio para teste rápido
            if len(domain) > 8:
                domain = random.sample(domain, 8)
            variables_info[var] = {
                'course': c,
                'class': course_to_class[c],
                'teacher': course_to_teacher.get(c),
                'index': i,
                'domain': domain
            }
            problem.addVariable(var, domain)

    vars_list = list(variables_info.keys())

    # mesmo slot+room não pode repetir para aulas da mesma turma
    for cls, cls_vars in defaultdict(list, {meta['class']: [] for meta in variables_info.values()}).items():
        cls_vars = [v for v, meta in variables_info.items() if meta['class'] == cls]
        for v1, v2 in itertools.combinations(cls_vars, 2):
            problem.addConstraint(lambda a,b: a != b, (v1,v2))

    # professor não pode ter duas aulas no mesmo slot
    for v1, v2 in itertools.combinations(vars_list, 2):
        t1 = variables_info[v1]['teacher']
        t2 = variables_info[v2]['teacher']
        if t1 and t1 == t2:
            problem.addConstraint(lambda a,b: a[0] != b[0], (v1,v2))

    # professor indisponível
    for var, meta in variables_info.items():
        t = meta['teacher']
        if t in data.get('tr', {}):
            forbidden = set(data['tr'][t])
            problem.addConstraint(lambda pair, f=forbidden: pair[0] not in f, (var,))

    # aulas online devem ser no mesmo dia
    online_vars = [f"{c}_{idx}" for c, idx in online_info.items() if f"{c}_{idx}" in variables_info]
    if online_vars:
        def same_day(*assigned):
            days = [day_of_slot(a[0]) for a in assigned]
            return len(set(days))==1
        problem.addConstraint(same_day, tuple(online_vars))

    # duas aulas do mesmo curso não no mesmo slot
    for c in course_list:
        v1, v2 = f"{c}_1", f"{c}_2"
        if v1 in variables_info and v2 in variables_info:
            problem.addConstraint(lambda a,b: a[0] != b[0], (v1,v2))

    return problem, variables_info, rooms
