import pandas as pd
import numpy as np
import random


def parse_tsp(file_path):
    # Read the file line by line
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    is_node_coord = False

    for line in lines:
        line = line.strip()
        if line == "EOF":
            break

        # Extract data if we are in the coordinates section
        if is_node_coord:
            parts = line.split()
            if len(parts) >= 3:
                node_id = int(parts[0])  # Ordering number
                x_coord = float(parts[1])  # X location
                y_coord = float(parts[2])  # Y location
                data.append([node_id, x_coord, y_coord])

        # Detect the start of the coordinates section
        elif line == "NODE_COORD_SECTION":
            is_node_coord = True

    # Load the data into a pandas dataframe for easy access
    df = pd.DataFrame(data, columns=['City_ID', 'X', 'Y'])
    df.set_index('City_ID', inplace=True)

    return df


def calculate_distance(city1, city2):
    # Extract coordinates from the pandas series
    x1, y1 = city1['X'], city1['Y']
    x2, y2 = city2['X'], city2['Y']

    # Euclidean distance formula
    distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return float(distance)


def generate_random_solution(df):
    # Create a python list of city IDs and shuffle it
    cities = list(df.index)
    random.shuffle(cities)
    return cities


def verify_solution(solution, df):
    original_cities = set(df.index)
    solution_cities = set(solution)

    # Check if length is correct and sets match (no repetition, all included)
    is_valid = (len(solution) == len(df)) and (original_cities == solution_cities)

    if is_valid:
        print("Status: VALID - All cities are included and there is no repetition.")
    else:
        print("Status: INVALID - Solution is corrupted.")

    return is_valid


# Main execution block to test all functionalities
if __name__ == "__main__":
    # 1. Parse the TSP file
    file_name = "berlin11_modified.tsp"
    print(f"--- Loading data from {file_name} ---")
    df_cities = parse_tsp(file_name)
    print(df_cities.head())
    print("\n")

    # 2. Calculate distance between two specific cities (e.g., City 1 and City 2)
    dist = calculate_distance(df_cities.loc[1], df_cities.loc[2])
    print(f"--- Calculating Distance ---")
    print(f"Distance between City 1 and City 2: {dist:.2f}")
    print("\n")

    # 3. Generate a random solution
    print(f"--- Generating Random Solution ---")
    random_route = generate_random_solution(df_cities)
    print(f"Generated Route: {random_route}")
    print("\n")

    # 4. Verify the solution
    print(f"--- Verifying the Solution ---")
    verify_solution(random_route, df_cities)
    
