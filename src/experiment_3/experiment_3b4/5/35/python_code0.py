import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Number of periods
N = len(data['price'])

# Create the LP problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(N)]

# Objective function
profit = pulp.lpSum([
    data['price'][n] * sellquantity[n] - 
    data['cost'][n] * buyquantity[n] - 
    data['holding_cost'] * stock[n] 
    for n in range(N)
])
problem += profit

# Constraints
# Initial stock
problem += stock[0] == 0  # stock_0 = 0

# Stock balance and capacity constraints
for n in range(N):
    if n > 0:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]
    problem += stock[n] <= data['capacity']

# Ending stock constraint
problem += stock[N-1] == 0  # stock_N = 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')