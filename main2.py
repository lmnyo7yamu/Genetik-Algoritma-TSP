import pandas as pd
import math
import random


# 1. Parse TSP File
def parse_tsp(file_path):
    cities = []
    with open(file_path, 'r') as file:
        started = False
        for line in file:
            if line.strip() == "EOF": break
            if line.strip() == "NODE_COORD_SECTION":
                started = True
                continue
            if started:
                parts = line.split()
                if len(parts) >= 3:
                    cities.append({'id': int(parts[0]), 'x': float(parts[1]), 'y': float(parts[2])})
    return pd.DataFrame(cities)


# 2. Calculate Distance
def calculate_distance(city1, city2):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


# 4. Generate Random Solution
def generate_random_solution(df_cities):
    ids = df_cities['id'].tolist()
    return random.sample(ids, len(ids))


# 5. Calculate Fitness
def calculate_fitness(solution, df_cities):
    total = 0.0
    n = len(solution)
    for i in range(n):
        c1 = df_cities[df_cities['id'] == solution[i]].iloc[0]
        c2 = df_cities[df_cities['id'] == solution[(i + 1) % n]].iloc[0]
        total += calculate_distance(c1, c2)
    return total


# 6. Print Info
def print_solution(solution, score, title):
    route = " ".join(str(i) for i in solution)
    print(f"{title} | Score: {score:.2f} | Route: {route}")


# 7. Greedy Algorithm
def greedy_tsp(df_cities, start_id):
    unvisited = df_cities['id'].tolist()
    current = start_id
    route = [current]
    unvisited.remove(current)

    while unvisited:
        curr_city = df_cities[df_cities['id'] == current].iloc[0]
        nearest = None
        min_dist = float('inf')

        for candidate in unvisited:
            cand_city = df_cities[df_cities['id'] == candidate].iloc[0]
            dist = calculate_distance(curr_city, cand_city)
            if dist < min_dist:
                min_dist = dist
                nearest = candidate

        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return route


# 8, 9, 10. Run Experiments
def run_experiments(file_path):
    print(f"\n--- Testing: {file_path} ---")
    df = parse_tsp(file_path)

    # 8. Greedy Test
    best_greedy_score = float('inf')
    best_greedy_route = []

    for start_id in df['id']:
        route = greedy_tsp(df, start_id)
        score = calculate_fitness(route, df)
        if score < best_greedy_score:
            best_greedy_score = score
            best_greedy_route = route

    print_solution(best_greedy_route, best_greedy_score, "Best Greedy")

    # 9. Random Test
    random_scores = []
    for _ in range(100):
        random_scores.append(calculate_fitness(generate_random_solution(df), df))

    best_random = min(random_scores)
    print(f"Best Random Score: {best_random:.2f}")
    print(f"Greedy is better than Random by: {best_random - best_greedy_score:.2f}")


if __name__ == "__main__":
    run_experiments('berlin11_modified.tsp')
    run_experiments('berlin52.tsp')