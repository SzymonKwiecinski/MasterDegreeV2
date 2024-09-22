import pulp
import json

# Data input
data = json.loads('{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}')

# Extracting data from JSON
time = data['time']  # matrix of time required for each part in each shop
profit = data['profit']  # profit for each part
capacity = data['capacity']  # capacity of each shop

# Number of spare parts and shops
K = len(profit)
S = len(capacity)

# Create a linear programming problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Output results
quantity = [x[k].varValue for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')