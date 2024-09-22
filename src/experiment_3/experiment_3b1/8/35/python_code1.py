import pulp
import json

# Data input
data_json = """{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}"""
data = json.loads(data_json)

# Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Problem Definition
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(1, N + 1)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(1, N + 1)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(1, N + 1)]

# Objective Function
problem += pulp.lpSum(prices[n - 1] * sellquantity[n - 1] - costs[n - 1] * buyquantity[n - 1] - holding_cost * stock[n - 1] for n in range(1, N + 1))

# Stock Balance Constraints
initial_stock = 0
for n in range(1, N + 1):
    if n == 1:
        problem += stock[n - 1] == initial_stock + buyquantity[n - 1] - sellquantity[n - 1]
    else:
        problem += stock[n - 1] == stock[n - 2] + buyquantity[n - 1] - sellquantity[n - 1]

# Capacity Constraints
for n in range(1, N + 1):
    problem += stock[n - 1] <= capacity

# Final Stock Requirement
problem += stock[N - 1] == 0

# Solve the problem
problem.solve()

# Print results
buyquantity_values = [pulp.value(buyquantity[n]) for n in range(N)]
sellquantity_values = [pulp.value(sellquantity[n]) for n in range(N)]
stock_values = [pulp.value(stock[n]) for n in range(N)]

print(f'Buying Quantities: {buyquantity_values}')
print(f'Selling Quantities: {sellquantity_values}')
print(f'Stock Levels: {stock_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')