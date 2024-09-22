import pulp

# Data from the problem
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
    "maintain": [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ],
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Factory_Profit", pulp.LpMaximize)

# Constants
num_products = len(data["profit"])
num_months = len(data["maintain"])
num_machines = len(data["num_machines"])
days_in_month = 24

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')

# Objective Function
profit_contribution = pulp.lpSum(data["profit"][k] * sell[k, i] for k in range(num_products) for i in range(num_months))
storage_cost = pulp.lpSum(data["store_price"] * storage[k, i] for k in range(num_products) for i in range(num_months))
problem += profit_contribution - storage_cost

# Constraints
for i in range(num_months):
    for m in range(num_machines):
        problem += pulp.lpSum(data["time"][k][m] * manufacture[k, i] for k in range(num_products)) <= (
            (data["num_machines"][m] - data["maintain"][i][m]) * data["n_workhours"] * days_in_month
        )

for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += manufacture[k, i] == sell[k, i] + storage[k, i]
        else:
            problem += manufacture[k, i] + storage[k, i-1] == sell[k, i] + storage[k, i]

        problem += sell[k, i] <= data["limit"][k][i]

problem += pulp.lpSum(storage[k, num_months - 1] for k in range(num_products)) >= data["keep_quantity"] * num_products

# Solve the problem
problem.solve()

# Prepare output
output = {
    "sell": [[pulp.value(sell[k, i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k, i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k, i]) for k in range(num_products)] for i in range(num_months)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')