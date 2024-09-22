import pulp
import json

# Input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Problem parameters
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buy", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", range(N), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(sellquantity[n] * prices[n] - buyquantity[n] * costs[n] - holding_cost * stock[n] for n in range(N))
problem += profit

# Constraints
initial_stock = 0
for n in range(N):
    if n == 0:
        problem += stock[n] == initial_stock + buyquantity[n] - sellquantity[n]
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]
    problem += stock[n] <= capacity

# Final stock must be zero
problem += stock[N-1] == 0

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buyquantity": [buyquantity[n].varValue for n in range(N)],
    "sellquantity": [sellquantity[n].varValue for n in range(N)],
    "stock": [stock[n].varValue for n in range(N)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')