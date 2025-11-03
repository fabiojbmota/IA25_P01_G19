from parser_ import parse_dataset
from model import build_problem
from solver import find_best_solution, print_solution
import time

def main():
    dataset_path = "ClassTT_01_tiny.txt"
    print("A carregar dataset:", dataset_path)
    data = parse_dataset(dataset_path)

    rooms = ["Lab01","RoomA","RoomB","RoomC","RoomD"]

    print("A construir problema...")
    problem, variables_info, rooms_used = build_problem(data, rooms=rooms, lessons_per_course=2)

    print("Número de variáveis:", len(variables_info))
    example_var = next(iter(variables_info))
    print("Domínio exemplo:", variables_info[example_var]['domain'])

    print("A resolver...")
    t0 = time.time()
    best, score, n_sols = find_best_solution(problem, variables_info, max_solutions=50)
    t1 = time.time()
    print(f"Tempo: {t1-t0:.2f}s, soluções examinadas: {n_sols}")

    if best:
        print("Melhor solução encontrada (pontuação):", score)
        print_solution(best, variables_info)
    else:
        print("Nenhuma solução encontrada")

if __name__=="__main__":
    main()
