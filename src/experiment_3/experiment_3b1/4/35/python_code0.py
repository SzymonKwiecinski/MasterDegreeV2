import pulp
import json

# Data from the input
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Parameters
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Create the problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("buy_quantity", range(N), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("sell_quantity", range(N), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("stock", range(N), lowBound=0, upBound=C, cat='Continuous')

# Objective function
problem += pulp.lpSum(p[n] * s[n] - c[n] * b[n] - h * x[n] for n in range(N))

# Constraints
problem += (x[0] == 0, "Initial_Stock_Zero")

for n in range(1, N):
    problem += (x[n] == x[n-1] + b[n-1] - s[n-1], f"Stock_Balance_{n}")

for n in range(N):
    problem += (x[n] <= C, f"Capacity_Constraint_{n}")

problem += (x[N-1] == 0, "Final_Stock_Zero")

# Solve the problem
problem.solve()

# Output results
buyquantity = [b[n].varValue for n in range(N)]
sellquantity = [s[n].varValue for n in range(N)]
stock = [x[n].varValue for n in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Buy Quantity: {buyquantity}')
print(f'Sell Quantity: {sellquantity}')
print(f'Stock: {stock}')