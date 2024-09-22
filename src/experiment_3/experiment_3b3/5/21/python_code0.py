import pulp

# Data from the problem
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
    'down': [[0, 1, 1, 1, 1]],
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

M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), cat='Binary')

# Objective Function: Maximize profits
profit_terms = (
    pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in range(K) for i in range(I))
)

problem += profit_terms

# Constraints
for i in range(I):
    for m in range(M):
        available_time = data['n_workhours'] * (24 - data['down'][0][m])
        problem += (
            pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K)) <= available_time,
            f"Production_Time_Constraint_m{m}_i{i}"
        )

for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= data['limit'][k][i], f"Sales_Limit_k{k}_i{i}"

for k in range(K):
    for i in range(1, I):
        problem += (
            storage[k, i] == storage[k, i - 1] + manufacture[k, i] - sell[k, i],
            f"Storage_Balance_k{k}_i{i}"
        )

for k in range(K):
    problem += (
        storage[k, I - 1] >= data['keep_quantity'],
        f"Ending_Inventory_Requirement_k{k}"
    )

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')