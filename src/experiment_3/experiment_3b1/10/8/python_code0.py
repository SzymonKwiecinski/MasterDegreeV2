import pulp
import json

# Data in JSON format
data = '{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}'
data = json.loads(data)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define the number of spare parts and shops
num_parts = data['NumParts']
num_machines = data['NumMachines']

# Create decision variables for quantity of each spare part produced
quantity = pulp.LpVariable.dicts("Quantity", range(num_parts), lowBound=0)

# Define the objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(num_parts)), "Total_Profit"

# Define the constraints based on shop capacities
for s in range(num_machines):
    problem += pulp.lpSum(data['Time'][k][s] * quantity[k] for k in range(num_parts)) <= data['Capacity'][s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')