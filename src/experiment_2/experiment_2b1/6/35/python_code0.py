import pulp
import json

# Input data in JSON format
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Define problem
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

# Parameters
N = len(data['price'])  # Number of periods
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Decision variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(N)]

# Objective function
profit = pulp.lpSum([(prices[n] - costs[n]) * sellquantity[n] - holding_cost * stock[n] for n in range(N)])
problem += profit

# Constraints
problem += (pulp.lpSum(buyquantity) <= capacity, "Capacity_Constraint")  # Total buying should not exceed capacity

# Stock balance constraints
for n in range(N):
    if n == 0:
        problem += (stock[n] == buyquantity[n] - sellquantity[n], f'Stock_Balance_{n}')
    else:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f'Stock_Balance_{n}')

# Final stock must be zero
problem += (stock[N-1] == 0, "Final_Stock_Constraint")

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

# Print results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')