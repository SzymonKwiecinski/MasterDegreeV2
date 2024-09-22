import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Extracting data
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buy_quantity = [pulp.LpVariable(f"buy_quantity_{n}", 0, capacity) for n in range(N)]
sell_quantity = [pulp.LpVariable(f"sell_quantity_{n}", 0, capacity) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", 0, capacity) for n in range(N+1)]

# Objective Function
profit = pulp.lpSum([prices[n] * sell_quantity[n] - costs[n] * buy_quantity[n] - holding_cost * stock[n+1] for n in range(N)])
problem += profit

# Constraints

# Initial stock is zero
problem += stock[0] == 0

# Stock flow constraints
for n in range(N):
    problem += stock[n] + buy_quantity[n] - sell_quantity[n] == stock[n+1]

# Final stock is zero
problem += stock[N] == 0

# Solve
problem.solve()

# Output
output = {
    "buyquantity": [pulp.value(buy_quantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell_quantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n+1]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')