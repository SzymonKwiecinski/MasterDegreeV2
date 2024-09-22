import pulp

# Data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Create a linear programming problem
problem = pulp.LpProblem("Commodity_Trading_Problem", pulp.LpMaximize)

N = len(data['price'])

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(1, N + 1), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("sellquantity", range(1, N + 1), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", range(0, N + 1), lowBound=0, cat='Continuous')

# Objective function
objective = pulp.lpSum([data['price'][n-1] * sellquantity[n] - data['cost'][n-1] * buyquantity[n] - data['holding_cost'] * stock[n] for n in range(1, N + 1)])
problem += objective

# Constraints

# Initial stock constraint
problem += stock[0] == 0

# Final stock constraint
problem += stock[N] == 0

# Capacity constraints
for n in range(1, N + 1):
    problem += stock[n] <= data['capacity']

# Stock balance constraints
for n in range(1, N + 1):
    problem += stock[n-1] + buyquantity[n] - sellquantity[n] == stock[n]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')