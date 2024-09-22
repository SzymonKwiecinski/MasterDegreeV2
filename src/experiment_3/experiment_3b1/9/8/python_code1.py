import pulp
import json

# Data input
data = json.loads('{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}')

# Parameters
K = data['NumParts']  # Number of spare parts
S = data['NumMachines']  # Number of shops
time = data['Time']  # Time required for each part in each shop
profit = data['Profit']  # Profit for each part
capacity = data['Capacity']  # Capacity for each shop

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the results
result_quantities = [quantity[k].varValue for k in range(K)]
print(f'Output: {{ quantity = {result_quantities} }}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')