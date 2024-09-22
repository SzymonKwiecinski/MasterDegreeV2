import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Extract data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Initialize the problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, cat='Continuous') for n in range(N + 1)]

# Objective Function
profit_expr = [
    price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n]
    for n in range(N)
]
problem += pulp.lpSum(profit_expr)

# Initial and final stock constraints
problem += stock[0] == 0
problem += stock[N] == 0

# Constraints
for n in range(N):
    # Stock balance constraint
    problem += stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n]
    # Capacity constraint
    problem += buyquantity[n] + stock[n - 1] - sellquantity[n] <= capacity

# Solve
problem.solve()

# Print objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')