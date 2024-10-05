import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])  # Number of periods

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, upBound=data['capacity'], cat='Continuous') for n in range(N)]

# Objective function
objective = pulp.lpSum([data['price'][n] * sellquantity[n] - data['cost'][n] * buyquantity[n] - data['holding_cost'] * stock[n] for n in range(N)])
problem += objective

# Constraints
# Stock balance constraints
problem += stock[0] == buyquantity[0] - sellquantity[0]
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

# Initial stock
problem += stock[0] == 0

# Capacity constraints
for n in range(N):
    problem += stock[n] <= data['capacity']

# Ending stock
problem += stock[N-1] == 0

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')