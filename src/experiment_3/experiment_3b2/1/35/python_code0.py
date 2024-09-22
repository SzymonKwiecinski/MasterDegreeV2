import pulp
import json

# Data extracted from the provided JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the linear programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum(price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N))

# Constraints
problem += (stock[0] == buyquantity[0] - sellquantity[0])

for n in range(1, N):
    problem += (stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n])

for n in range(N):
    problem += (stock[n] <= capacity)

problem += (stock[N - 1] == 0)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')