import pulp
import json

# Input data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Extracting data from input
num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variable for the quantity of each part
quantity = pulp.LpVariable.dicts("quantity", range(num_parts), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(num_parts)])

# Constraints for each machine's capacity
for s in range(num_machines):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(num_parts)]) <= capacity[s], f"Capacity_Constraint_Machine_{s}"

# Solve the problem
problem.solve()

# Output the quantity of each spare part
result = {"quantity": [quantity[k].varValue for k in range(num_parts)]}
print(result)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')