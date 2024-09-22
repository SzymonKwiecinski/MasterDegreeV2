import pulp
import json

# Given data in JSON format
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Extracting data
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Create the problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Buy_Quantity", range(1, N + 1), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("Sell_Quantity", range(1, N + 1), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("Stock", range(0, N + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(p[n - 1] * y[n] - c[n - 1] * x[n] - h * S[n] for n in range(1, N + 1))

# Constraints
# Capacity constraint
for n in range(1, N + 1):
    problem += S[n] <= C

# Stock balance equation
for n in range(1, N + 1):
    if n == 1:
        problem += S[n] == x[n] - y[n]
    else:
        problem += S[n] == S[n - 1] + x[n] - y[n]

# Final stock must be zero
problem += S[N] == 0

# Solve the problem
problem.solve()

# Print results
buy_quantity = [x[n].varValue for n in range(1, N + 1)]
sell_quantity = [y[n].varValue for n in range(1, N + 1)]
stock = [S[n].varValue for n in range(0, N + 1)]

print(f'Buy Quantity: {buy_quantity}')
print(f'Sell Quantity: {sell_quantity}')
print(f'Stock: {stock}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')