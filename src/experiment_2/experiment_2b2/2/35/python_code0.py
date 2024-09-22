import pulp

# Data from input
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

# Define the LP problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Define decision variables
buyquantity = [pulp.LpVariable(f"buy_q_{n}", lowBound=0, cat='Continuous') for n in range(N)]
sellquantity = [pulp.LpVariable(f"sell_q_{n}", lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0, upBound=capacity, cat='Continuous') for n in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum([(price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints

# Stock flow constraints
for n in range(N):
    if n == 0:
        # Initial stock is 0
        problem += (buyquantity[n] - sellquantity[n] == stock[n])
    else:
        problem += (stock[n-1] + buyquantity[n] - sellquantity[n] == stock[n])

# Final stock must be 0
problem += stock[-1] == 0

# Solve the problem
problem.solve()

# Prepare and print results
result = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

import json
print(json.dumps(result))
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')