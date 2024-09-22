import pulp
import json

# Input data
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Extracting data from the input
num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity of each part to be made
quantity = pulp.LpVariable.dicts("quantity", range(num_parts), lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(num_parts)), "Total_Profit"

# Constraints: Shop capacity constraints
for s in range(num_machines):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(num_parts)) <= capacity[s], f"Capacity_Constraint_Shop_{s+1}"

# Solve the problem
problem.solve()

# Output the result
result = {"quantity": [quantity[k].varValue for k in range(num_parts)]}
print(json.dumps(result))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')