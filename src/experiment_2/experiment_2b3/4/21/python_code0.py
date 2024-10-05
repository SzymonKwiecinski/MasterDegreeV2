import pulp

# Data provided by the user
data = {
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    "down": [0, 1, 1, 1, 1],
    "limit": [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0
}

# Extract data dimensions
num_machines = data["num_machines"]
profit = data["profit"]
time = data["time"]
down = data["down"]
limit = data["limit"]
store_price = data["store_price"]
keep_quantity = data["keep_quantity"]
n_workhours = data["n_workhours"]

K = len(profit)
M = len(num_machines)
I = len(limit[0])

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(K)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    # Initial storage constraints
    problem += storage[k, 0] == 0  # No initial stock
    
    for i in range(I):
        # Manufacturing constraints
        problem += manufacture[k, i] <= limit[k][i]
        
        # Selling and storage balance
        if i == 0:
            problem += storage[k, i] + sell[k, i] == manufacture[k, i]
        else:
            problem += storage[k, i] + sell[k, i] == storage[k, i-1] + manufacture[k, i]
        
        # End month storage requirements
        problem += storage[k, I-1] == keep_quantity

# Machine time constraints
for i in range(I):
    for m in range(M):
        working_hours = num_machines[m] * 6 * n_workhours * 24 - maintain[m, i] * n_workhours
        problem += pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(K)) <= working_hours

# Machine maintenance constraints
for m in range(M):
    problem += pulp.lpSum(maintain[m, k] for k in range(K)) >= down[m]

# Solve the problem
problem.solve()

# Extract solution values
sell_values = [[pulp.value(sell[k, i]) for i in range(I)] for k in range(K)]
manufacture_values = [[pulp.value(manufacture[k, i]) for i in range(I)] for k in range(K)]
storage_values = [[pulp.value(storage[k, i]) for i in range(I)] for k in range(K)]
maintain_values = [[pulp.value(maintain[m, k]) for m in range(M)] for k in range(K)]

# Output format
solution = {
    "sell": sell_values,
    "manufacture": manufacture_values,
    "storage": storage_values,
    "maintain": maintain_values
}

# Print the solution and objective
print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')