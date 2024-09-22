import pulp
import json

# Input data
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Parameters
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Create the problem
problem = pulp.LpProblem("Warehouse_Operation_Problem", pulp.LpMaximize)

# Decision variables
b = [pulp.LpVariable(f'b_{n}', lowBound=0) for n in range(N)]
s = [pulp.LpVariable(f's_{n}', lowBound=0) for n in range(N)]
x = [pulp.LpVariable(f'x_{n}', lowBound=0) for n in range(N)]

# Objective function
profit = pulp.lpSum(p[n] * s[n] - c[n] * b[n] - h * x[n] for n in range(N))
problem += profit

# Constraints
# Stock balance constraints
for n in range(N):
    if n == 0:
        problem += x[0] == b[0] - s[0]
    else:
        problem += x[n] == x[n-1] + b[n] - s[n]

# Capacity constraints
for n in range(N):
    problem += x[n] <= C

# Non-negativity constraints (already defined by pulp.LpVariable)

# Final stock must be zero
problem += x[N-1] == 0

# Solve the problem
problem.solve()

# Prepare output
buyquantity = [b[n].varValue for n in range(N)]
sellquantity = [s[n].varValue for n in range(N)]
stock = [x[n].varValue for n in range(N)]

# Print the objective value and results in the specified format
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps({"buyquantity": buyquantity, "sellquantity": sellquantity, "stock": stock}))