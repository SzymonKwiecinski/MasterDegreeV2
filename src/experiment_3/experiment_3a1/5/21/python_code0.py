import pulp
import json

# Data from the provided JSON
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
num_m = data['num_machines']
profit_k = data['profit']
time_k_m = data['time']
down_m = data['down'][0]
limit_k_i = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Sets
M = range(len(num_m))  # machines
K = range(len(profit_k))  # products
I = range(len(limit_k_i[0]))  # months

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (K, I), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (M, K), cat='Binary')

# Objective function
problem += pulp.lpSum(profit_k[k] * sell[k][i] for k in K for i in I) - \
           pulp.lpSum(store_price * storage[k][i] for k in K for i in I)

# Constraints
# 1. Sell limits
for k in K:
    for i in I:
        problem += pulp.lpSum(sell[k][i]) <= limit_k_i[k][i]

# 2. Machine time constraints
for m in M:
    for i in I:
        problem += pulp.lpSum(time_k_m[k][m] * manufacture[k][i] for k in K) <= \
                   n_workhours * (24 - down_m[m])
        
# 3. Storage dynamics
for k in K:
    for i in range(1, len(I)):
        problem += storage[k][i] == storage[k][i - 1] + manufacture[k][i] - sell[k][i]

# 4. Storage capacity
for k in K:
    for i in I:
        problem += storage[k][i] <= 100

# 5. Final storage requirement
for k in K:
    problem += storage[k][len(I) - 1] >= keep_quantity

# Solve the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')