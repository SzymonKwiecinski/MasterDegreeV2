import pulp

# Data from JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])

# Define the LP problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, upBound=data['capacity']) for n in range(N)]

# Objective function
problem += pulp.lpSum(
    (data['price'][n] * sellquantity[n] - data['cost'][n] * buyquantity[n] - data['holding_cost'] * stock[n]) 
    for n in range(N)
)

# Constraints
problem += stock[0] == 0  # Initial stock condition
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

problem += stock[N-1] == stock[0]  # stock_N = 0

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')