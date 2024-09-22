import pulp
import json

# Data input
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Operation_Problem", pulp.LpMaximize)

# Decision variables
b = [pulp.LpVariable(f'b_{n}', lowBound=0) for n in range(N)]  # buy quantities
s = [pulp.LpVariable(f's_{n}', lowBound=0) for n in range(N)]  # sell quantities
x = [pulp.LpVariable(f'x_{n}', lowBound=0) for n in range(N)]  # stock levels

# Objective function
problem += pulp.lpSum(prices[n] * s[n] - costs[n] * b[n] - holding_cost * x[n] for n in range(N))

# Constraints
# Stock balance and capacity constraints
for n in range(N):
    if n == 0:
        problem += x[n] == b[n] - s[n]  # For the first period
    else:
        problem += x[n] == x[n-1] + b[n] - s[n]  # For subsequent periods

    problem += x[n] <= capacity  # Capacity constraint
    problem += x[n] >= 0  # No negative stock

# Non-negativity constraints
for n in range(N):
    problem += b[n] >= 0
    problem += s[n] >= 0

# Final stock must be zero
problem += x[N-1] == 0

# Solve the problem
problem.solve()

# Output results
buy_quantity = [pulp.value(b[n]) for n in range(N)]
sell_quantity = [pulp.value(s[n]) for n in range(N)]
stock = [pulp.value(x[n]) for n in range(N)]

print(f'Buy quantity: {buy_quantity}')
print(f'Sell quantity: {sell_quantity}')
print(f'Stock levels: {stock}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')