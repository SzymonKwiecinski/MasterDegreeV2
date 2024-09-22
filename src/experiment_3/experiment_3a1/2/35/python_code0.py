import pulp
import json

# Data
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Number of periods
N = len(prices)

# Create the problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(1, N + 1), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(1, N + 1), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(0, N + 1), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[n - 1] * sellquantity[n] - costs[n - 1] * buyquantity[n] - holding_cost * stock[n] for n in range(1, N + 1))
problem += profit

# Constraints
# Initial stock
problem += stock[0] == 0

# Stock balance and capacity constraints
for n in range(1, N + 1):
    if n > 1:
        problem += stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n]
    problem += stock[n] <= capacity

# Final stock condition
problem += stock[N] == 0

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')