import pulp
import json

# Given JSON data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], 
              [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], 
              [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], 
              [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Parameters
M = range(len(data['num_machines']))
K = range(len(data['profit']))
I = range(len(data['limit'][0]))
H = 24 * 6 * 2  # Total working hours in a month
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']

# Create the problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in K for i in I), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in K for i in I), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in K for i in I), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in M for i in I), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k, i] for k in K for i in I) - pulp.lpSum(store_price * storage[k, i] for k in K for i in I)

# Constraints
# Production Time Constraint
for m in M:
    for i in I:
        if i > 0:  # Only consider operational months
            problem += (
                pulp.lpSum(time[k][m] * manufacture[k, i] for k in K) <= H * (1 - down[m]),
                f"Production_Time_Constraint_m{m}_i{i}"
            )

# Sales Limitation
for k in K:
    for i in I:
        problem += (sell[k, i] <= limit[i][k], f"Sales_Limitation_k{k}_i{i}")

# Storage Balance
for k in K:
    for i in range(1, len(I)):
        problem += (storage[k, i] == storage[k, i - 1] + manufacture[k, i] - sell[k, i], f"Storage_Balance_k{k}_i{i}")

# Desired Ending Stock
for k in K:
    problem += (storage[k, len(I) - 1] >= keep_quantity, f"Desired_Ending_Stock_k{k}")

# Maintenance Constraints
for i in I:
    problem += (pulp.lpSum(maintain[m, i] for m in M) <= sum(down), f"Maintenance_Constraints_i{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')