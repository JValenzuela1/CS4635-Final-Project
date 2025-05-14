import os
import matplotlib.pyplot as plt
import numpy as np

def parse_summary_file(file_path):
    summary_data = {}

    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Extract relevant information from the file
    current_section = None
    for line in lines:
        line = line.strip()

        if line.startswith("Summary:"):
            current_section = "summary"
        elif line.startswith("Nondominated point set:"):
            current_section = "nondominated"
        elif line.startswith("Efficient point set:"):
            current_section = "efficient"
        elif line.startswith("Full database of objective values observed:"):
            current_section = "objective_values"
        elif line.startswith("Full database of evaluated design points:"):
            current_section = "design_points"
        
        # Extract number of nondominated points
        if current_section == "summary" and "Number of nondominated/efficient points:" in line:
            num_points = int(line.split(":")[-1].strip())
            summary_data['num_points'] = num_points

        # Add logic here to extract more values like RMSE or discrepancy if needed
        # For now, let's assume average solutions are part of the summary
        if current_section == "summary" and "Total number of function evaluations:" in line:
            total_evaluations = int(line.split(":")[-1].strip())
            summary_data['total_evaluations'] = total_evaluations

    return summary_data

def parse_filename(filename):
    # Extract p_value and budget from the filename
    parts = filename.split('_')
    
    # Debugging: print out the parts of the filename to understand the format
    print(f"Parsing filename: {filename}")
    print(f"Parts: {parts}")
    
    # Check if the filename follows the expected format
    if len(parts) < 3:
        print(f"Warning: Filename '{filename}' does not match the expected format. Skipping.")
        return None, None  # Return None if the filename is not in the expected format
    
    try:
        p_value = parts[1][1:]  # Extract after 'p'
        budget = parts[2].split('.')[0]  # Extract before '.txt'
        return p_value, budget
    except IndexError:
        print(f"Error: Could not parse filename '{filename}'.")
        return None, None  # Return None in case of parsing error

def analyze_results(results_dir):
    # Check and log the current working directory
    print(f"Current working directory: {os.getcwd()}")

    summary_data = {}
    valid_files_found = False  # Flag to track if any valid files were processed

    # Verify that the specified results directory exists
    if not os.path.isdir(results_dir):
        print(f"Error: The directory {results_dir} does not exist.")
        return summary_data  # Exit early if directory doesn't exist

    print(f"Processing files in directory: {results_dir}")

    # Loop over result files in the directory
    for filename in os.listdir(results_dir):
        if filename.endswith(".txt"):
            p_value, budget = parse_filename(filename)
            
            # Skip files that couldn't be parsed
            if p_value is None or budget is None:
                print(f"Skipping file (invalid format): {filename}")
                continue
            
            valid_files_found = True  # Found a valid file
            file_path = os.path.join(results_dir, filename)
            print(f"Processing file: {filename}")

            # Parse the file and get the summary data
            file_data = parse_summary_file(file_path)

            # Store results in summary_data dictionary
            key = f"p{p_value}_b{budget}"
            summary_data[key] = file_data

    # After processing, check if any valid files were found
    if not valid_files_found:
        print("No valid files found for processing.")

    return summary_data



def generate_graphs(summary_data):
    p_values = [2, 3, 4]
    budgets = [1000, 1500, 2000]
    
    # Loop through p_values to process data
    for p_value in p_values:
        avg_solutions = []  # To store average solution counts for each p
        rmse_values = []  # To store RMSE values
        discrepancy_values = []  # To store discrepancy values
        
        for budget in budgets:
            key = f"p{p_value}_b{budget}"
            if key in summary_data:
                avg_solutions.append(summary_data[key].get('num_points', 0))  # Using 'num_points' for now
                # Add logic to get RMSE and discrepancy if required
                rmse_values.append(0)  # Replace with actual logic for RMSE
                discrepancy_values.append(0)  # Replace with actual logic for discrepancy
            else:
                print(f"Warning: No data found for {key}.")
        
        # Debugging: Check if lists are populated
        print(f"p={p_value}, avg_solutions={avg_solutions}, rmse_values={rmse_values}, discrepancy_values={discrepancy_values}")
        
        # Proceed with plotting only if lists are not empty
        if avg_solutions:
            plt.plot(budgets, avg_solutions, marker='o', color='b', label=f'P={p_value}')
            plt.xlabel('Budget')
            plt.ylabel('Average Number of Solutions')
            plt.title(f'Average Solutions for P={p_value}')
            plt.legend()
            plt.savefig(f'avg_solutions_p{p_value}.png')
            plt.clf()  # Clear the figure for the next plot

        if rmse_values:
            plt.plot(budgets, rmse_values, marker='o', color='r', label=f'P={p_value}')
            plt.xlabel('Budget')
            plt.ylabel('RMSE')
            plt.title(f'RMSE for P={p_value}')
            plt.legend()
            plt.savefig(f'rmse_p{p_value}.png')
            plt.clf()  # Clear the figure for the next plot

        if discrepancy_values:
            plt.plot(budgets, discrepancy_values, marker='o', color='g', label=f'P={p_value}')
            plt.xlabel('Budget')
            plt.ylabel('Delaunay Discrepancy')
            plt.title(f'Delaunay Discrepancy for P={p_value}')
            plt.legend()
            plt.savefig(f'discrepancy_p{p_value}.png')
            plt.clf()  # Clear the figure for the next plot

def main():
    results_dir = '../results/'
    
    # Analyze results from the directory
    summary_data = analyze_results(results_dir)

    # Generate graphs based on summary data
    generate_graphs(summary_data)

if __name__ == '__main__':
    main()
