import pulp
import json

# Data from JSON
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

# Sets
M = range(len(data['num_machines']))  # machines
K = range(len(data['profit']))         # products
I = range(len(data['limit'][0]))       # months

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (K, I), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (M, K), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in K for i in I) - pulp.lpSum(data['store_price'] * storage[k][i] for k in K for i in I)

# Constraints
# Production Time Constraint
for k in K:
    for i in I:
        problem += (pulp.lpSum(data['time[i][m]'] * manufacture[k][i] for m in M) <= 
                     data['n_workhours'] * (1 - pulp.lpSum(maintain[m][k] for m in M)), f"Production_Time_Constraint_k{str(k)}_i{str(i)}")

# Maintenance Constraint
for m in M:
    for k in K:
        problem += maintain[m][k] <= data['down'][0][m], f"Maintenance_Constraint_m{str(m)}_k{str(k)}"

# Marketing Limitations
for k in K:
    for i in I:
        problem += sell[k][i] <= data['limit'][k][i], f"Marketing_Limitations_k{str(k)}_i{str(i)}"

# Storage Constraints
for k in K:
    for i in range(1, len(I)):
        problem += (storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i],
                     f"Storage_Constraint_k{str(k)}_i{str(i)}")
        problem += storage[k][i] <= 100, f"Storage_Limit_k{str(k)}_i{str(i)}"

# Ending Stock Requirement
for k in K:
    problem += storage[k][len(I)-1] >= data['keep_quantity'], f"Ending_Stock_Requirement_k{str(k)}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')