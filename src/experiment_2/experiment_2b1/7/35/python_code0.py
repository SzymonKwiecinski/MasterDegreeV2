import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Variables for buying, selling and stock for each period
buyquantity = [pulp.LpVariable(f'buy_{n}', lowBound=0, cat='Continuous') for n in range(N)]
sellquantity = [pulp.LpVariable(f'sell_{n}', lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Objective function: Total profit
profit = pulp.lpSum([(price[n] * sellquantity[n]) - (cost[n] * buyquantity[n]) - (holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n]
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]
    
    problem += stock[n] <= capacity  # stock cannot exceed capacity

# Last period constraint: warehouse must be empty
problem += stock[N-1] == 0

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')