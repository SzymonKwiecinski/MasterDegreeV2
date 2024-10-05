import pulp

# Data from the JSON input
data = {
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    "maintain": [[1, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 2, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]],
    "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]],
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0
}

# Problem parameters
num_m = data["num_machines"]
profits = data["profit"]
times = data["time"]
maintains = data["maintain"]
limits = data["limit"]
store_price = data["store_price"]
keep_quantity = data["keep_quantity"]
n_workhours = data["n_workhours"]

# Number of months, products, and machines
I = len(maintains)
K = len(profits)
M = len(num_m)

# Days and hours constants
days_per_month = 24
hours_per_month = days_per_month * n_workhours

# Create the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
problem += pulp.lpSum(profits[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I)), "Total_Profit"

# Constraints
for i in range(I):
    for m in range(M):
        problem += pulp.lpSum(times[k][m] * manufacture[k, i] for k in range(K) if m < len(times[k])) <= (num_m[m] - maintains[i][m]) * hours_per_month, f"Machine_Capacity_{i}_{m}"

for i in range(I):
    for k in range(K):
        problem += sell[k, i] <= limits[k][i], f"Sales_Limit_{k}_{i}"

for i in range(I):
    for k in range(K):
        if i == 0:
            problem += manufacture[k, i] == sell[k, i] + storage[k, i], f"Balance_FirstMonth_{k}_{i}"
        else:
            problem += manufacture[k, i] + storage[k, i-1] == sell[k, i] + storage[k, i], f"Balance_{k}_{i}"

# End condition: Ensure stocks at the end of the last month
for k in range(K):
    problem += storage[k, I-1] == keep_quantity, f"End_Stock_{k}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "sell": [[sell[k, i].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[k, i].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[k, i].varValue for k in range(K)] for i in range(I)]
}

# Print outputs
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')