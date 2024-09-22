import pulp
import json

# Data in JSON format
data = json.loads('{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}')

# Extracting data from the JSON
K = data['NumParts']  # Number of spare parts
S = data['NumMachines']  # Number of shops
time = data['Time']  # Worker-hours required for each part in each shop
profit = data['Profit']  # Profit for each spare part
capacity = data['Capacity']  # Worker-hours available in each shop

# Create the linear programming problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_shop_{s+1}"

# Solve the problem
problem.solve()

# Display results
quantities = [quantity[k].varValue for k in range(K)]
print(f'Optimal quantities of each spare part: {quantities}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')