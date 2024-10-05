import pulp

# Load data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05],
    ],
    'down': [0, 1, 1, 1, 1],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60],
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0,
}

# Initialize problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Constants
I = len(data['limit'][0])  # Number of months
K = len(data['profit'])  # Number of products
M = len(data['num_machines'])  # Number of machine types
workhours_per_month = 24 * 6 * data['n_workhours']

# Variables
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), lowBound=0, cat='Integer')

# Objective function
profit_total = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I))
storage_costs = pulp.lpSum(data['store_price'] * storage[k][i] for k in range(K) for i in range(I))
problem += profit_total - storage_costs, "Total_Profit"

# Constraints

# Marketing limits
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][k][i], f"Marketing_Limit_{k}_{i}"

# Machine constraints with maintenance scheduling
for m in range(M):
    for i in range(I):
        available_machines = data['num_machines'][m] - (maintain[m][i] if i < len(data['down']) else 0)
        available_hours = available_machines * workhours_per_month
        problem += pulp.lpSum((data['time'][k][m] if m < len(data['time'][k]) else 0) * manufacture[k][i] for k in range(K)) <= available_hours, f"Machine_Hours_{m}_{i}"

# Maintenance requirements
for m in range(M):
    total_months_down = pulp.lpSum(maintain[m][i] for i in range(I))
    problem += total_months_down >= data['down'][m], f"Maintenance_Down_Machine_{m}"

# Inventory balance constraints
for k in range(K):
    # Initial inventory constraint
    problem += storage[k][0] == manufacture[k][0] - sell[k][0], f"Initial_Inventory_{k}"
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Inventory_Balance_{k}_{i}"
    # Final inventory constraint
    problem += storage[k][I-1] == data['keep_quantity'], f"Final_Inventory_{k}"

# Solve the problem
problem.solve()

# Collect results
result = {
    "sell": [[sell[k][i].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[k][i].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[k][i].varValue for k in range(K)] for i in range(I)],
    "maintain": [[maintain[m][i].varValue for m in range(M)] for i in range(I)],
}

print(result)
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")