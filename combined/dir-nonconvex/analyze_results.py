import os
import numpy as np
import matplotlib.pyplot as plt

# Parse the filename to extract p_value and budget
def parse_filename(filename):
    print(f"Parsing filename: {filename}")  # Debugging: print filename being parsed
    parts = filename.split('_')
    
    # Ensure the format is correct: samples_out_pX_YYYY.txt
    if len(parts) < 4:
        raise ValueError(f"Filename format is incorrect: {filename}")
    
    try:
        # Extract p_value (the number after 'p')
        p_value = int(parts[2][1:])  # Extract the number after 'p', e.g., p2, p3, p4
        # Extract budget (the number before '.txt')
        budget = int(parts[3].split('.')[0])  # e.g., 1000, 1500, 2000 (before .txt)
    except ValueError as e:
        print(f"Error parsing filename {filename}: {e}")
        raise
    
    return p_value, budget


# Read the file and extract the necessary data
def parse_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    num_points = None
    for line in lines:
        if "Number of nondominated/efficient points" in line:
            try:
                num_points = int(line.split(":")[1].strip())
            except ValueError:
                print(f"Could not parse number of points in {filepath}")
                num_points = 0
            break

    if num_points is None:
        print(f"'Number of nondominated/efficient points' not found in {filepath}")
        num_points = 0
    
    # Extract Nondominated point set
    nondominated_points = []
    reading_points = False
    for line in lines:
        if "Nondominated point set" in line:
            reading_points = True
        elif reading_points and line.strip() == "":
            break
        elif reading_points:
            try:
                point = list(map(float, line.split()))
                nondominated_points.append(point)
            except ValueError:
                print(f"Skipped malformed line in {filepath}: {line.strip()}")
    
    return num_points, nondominated_points


# Analyze the results in the directory
def analyze_results(results_dir):
    summary_data = {}

    for filename in os.listdir(results_dir):
        if filename.startswith("samples_out_p") and filename.endswith(".txt"):
            filepath = os.path.join(results_dir, filename)
            p_value, budget = parse_filename(filename)
            num_points, nondominated_points = parse_file(filepath)

            # If the p_value does not exist in the dictionary, initialize it
            if p_value not in summary_data:
                summary_data[p_value] = {}

            # Store the number of solutions
            summary_data[p_value][budget] = {
                "avg_solutions": num_points,
                "nondominated_points": nondominated_points
            }
    print(f"Parsed {filename} → P={p_value}, Budget={budget}, Points={num_points}")
    return summary_data

# Calculate RMSE
def calculate_rmse(actual, predicted):
    return np.sqrt(np.mean((np.array(actual) - np.array(predicted)) ** 2))

# Calculate Delaunay discrepancy
def calculate_delaunay_discrepancy(points):
    # For simplicity, we will just calculate the variance of the distances between points
    if len(points) < 2:
        return 0
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = np.linalg.norm(np.array(points[i]) - np.array(points[j]))
            distances.append(distance)
    
    return np.var(distances)

# Generate and save graphs
def generate_graphs(summary_data):
    output_dir = os.getcwd()

    for p_value, data in summary_data.items():
        budgets = [1000, 1500, 2000]
        avg_solutions = [data.get(budget, {}).get("avg_solutions", 0) for budget in budgets]

        # Combine all nondominated points across budgets to form the reference front
        all_points = []
        for budget in budgets:
            all_points.extend(data.get(budget, {}).get("nondominated_points", []))
        all_points = np.array(all_points)

        # Use the centroid of the union as reference point
        if len(all_points) > 0:
            reference_centroid = np.mean(all_points, axis=0)
        else:
            reference_centroid = None

        # Compute RMSE values to the reference centroid
        rmse_values = []
        for budget in budgets:
            current_points = data.get(budget, {}).get("nondominated_points", [])
            if current_points and reference_centroid is not None:
                curr_centroid = np.mean(current_points, axis=0)
                rmse = calculate_rmse(curr_centroid, reference_centroid)
            else:
                rmse = 0
            rmse_values.append(rmse)

        # Calculate Delaunay discrepancy for each budget
        delaunay_values = [
            calculate_delaunay_discrepancy(data.get(budget, {}).get("nondominated_points", []))
            for budget in budgets
        ]

        # Plotting Average Solutions
        plt.figure()
        plt.plot(budgets, avg_solutions, marker='o', color='b', label=f'P={p_value}')
        plt.title(f'Average Solutions for P={p_value}')
        plt.xlabel('Budget')
        plt.ylabel('Average Solutions')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{output_dir}/avg_solutions_p{p_value}.png")
        plt.close()

        # Plotting RMSE
        plt.figure()
        plt.plot(budgets, rmse_values, marker='o', color='g', label=f'P={p_value}')
        plt.title(f'RMSE to Combined Centroid for P={p_value}')
        plt.xlabel('Budget')
        plt.ylabel('RMSE')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{output_dir}/rmse_p{p_value}.png")
        plt.close()

        # Plotting Delaunay Discrepancy
        plt.figure()
        plt.plot(budgets, delaunay_values, marker='o', color='r', label=f'P={p_value}')
        plt.title(f'Delaunay Discrepancy for P={p_value}')
        plt.xlabel('Budget')
        plt.ylabel('Delaunay Discrepancy')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{output_dir}/delaunay_p{p_value}.png")
        plt.close()

        # Saving tables to a text file
        with open(f"{output_dir}/summary_table_p{p_value}.txt", "w") as f:
            f.write(f"Summary Table for P={p_value}\n")
            f.write(f"Budget - Avg Solutions, RMSE (to combined centroid), Delaunay Discrepancy\n")
            for i, budget in enumerate(budgets):
                f.write(f"{budget}: {avg_solutions[i]}, {rmse_values[i]}, {delaunay_values[i]}\n")

# Main function to execute everything
def main():
    results_dir = os.getcwd()  # Assuming the script is in the same folder as the results
    print(f"Current working directory: {results_dir}")
    
    summary_data = analyze_results(results_dir)
    generate_graphs(summary_data)

if __name__ == "__main__":
    main()
