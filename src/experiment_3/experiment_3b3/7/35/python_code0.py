import pulp

# Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extracting parameters
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Define the LP problem
problem = pulp.LpProblem("WarehouseOperation", pulp.LpMaximize)

# Define variables
b = [pulp.LpVariable(f'b_{n}', lowBound=0, cat='Continuous') for n in range(N)]
s = [pulp.LpVariable(f's_{n}', lowBound=0, cat='Continuous') for n in range(N)]
x = [pulp.LpVariable(f'x_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Objective function
problem += pulp.lpSum([p[n] * s[n] - c[n] * b[n] - h * x[n] for n in range(N)])

# Constraints
# Initial stock is assumed zero
problem += (x[0] == b[0] - s[0], "InitialStockConstraint")

# Inventory balance constraints
for n in range(1, N):
    problem += (x[n] == x[n-1] + b[n] - s[n], f"StockBalanceConstraint_{n}")

# Capacity constraints
for n in range(N):
    problem += (x[n] <= C, f"CapacityConstraint_{n}")

# Final stock constraint
problem += (x[N-1] == 0, "FinalStockConstraint")

# Solve the problem
problem.solve()

# Output the solution
for n in range(N):
    print(f"Period {n+1}: Buy = {pulp.value(b[n])}, Sell = {pulp.value(s[n])}, Stock = {pulp.value(x[n])}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')