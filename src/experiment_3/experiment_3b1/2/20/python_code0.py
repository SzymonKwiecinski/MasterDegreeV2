import pulp
import json

# Data from JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'maintain': [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Defining parameters
M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['maintain'])

# Problem definition
problem = pulp.LpProblem("Manufacturing_and_Selling", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] - data['store_price'] * storage[k][i] 
                      for k in range(K) for i in range(I)), "Total Profit"

# Production Time Constraints
for i in range(I):
    problem += (
        pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K) for m in range(M)) 
        <= (data['num_machines'][i] - sum(data['maintain'][i][m] for m in range(M))) * data['n_workhours'] * 24,
        f"Production_Time_Constraint_{i}"
    )

# Marketing Limitations
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][i][k], f"Marketing_Limit_{k}_{i}"

# Storage Constraints
for k in range(K):
    for i in range(I):
        problem += storage[k][i] <= 100, f"Storage_Constraint_{k}_{i}"

# Stock Requirements
for k in range(K):
    for i in range(I):
        problem += storage[k][i] == data['keep_quantity'], f"Stock_Requirement_{k}_{i}"

# Flow Balance
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i - 1] + manufacture[k][i] - sell[k][i], f"Flow_Balance_{k}_{i}"

# Non-negativity Constraints (already defined in decision variables)

# Solve the problem
problem.solve()

# Output result
output = {
    "sell": [[sell[k][i].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[k][i].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[k][i].varValue for k in range(K)] for i in range(I)]
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')