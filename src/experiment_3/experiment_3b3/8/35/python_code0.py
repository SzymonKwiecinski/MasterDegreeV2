import pulp

# Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Problem definition
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0, cat='Continuous') for n in range(1, N+1)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0, cat='Continuous') for n in range(1, N+1)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, cat='Continuous') for n in range(1, N+1)]

# Objective function
profit = pulp.lpSum([price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N)])
problem += profit

# Constraints

# Initial stock
problem += stock[0] == buyquantity[0] - sellquantity[0]

# Stock balance equation for rest of periods
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

# Capacity constraints
for n in range(N):
    problem += stock[n] <= capacity

# Sell quantity cannot exceed stock
for n in range(N):
    problem += sellquantity[n] <= stock[n]

# Final stock is zero
problem += stock[N-1] == 0

# Solve the problem
problem.solve()

# Output the results
print(f'Buy Quantities: {[pulp.value(bq) for bq in buyquantity]}')
print(f'Sell Quantities: {[pulp.value(sq) for sq in sellquantity]}')
print(f'Stock Levels: {[pulp.value(st) for st in stock]}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')