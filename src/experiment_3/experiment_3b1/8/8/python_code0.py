import pulp
import json

# Data provided in JSON format
data_json = '{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}'
data = json.loads(data_json)

# Defining parameters
K = data['NumParts']                # Number of spare parts
S = data['NumMachines']              # Number of shops
time = data['Time']                  # Worker-hours required for each part in each shop
profit = data['Profit']              # Profit for each part
capacity = data['Capacity']          # Capacity of each shop

# Create a Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)  # Quantity of each part produced

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')