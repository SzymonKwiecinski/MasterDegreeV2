import pulp

# Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Parameters
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Variables
b = [pulp.LpVariable(f'b_{n}', lowBound=0, cat='Continuous') for n in range(N)]
s = [pulp.LpVariable(f's_{n}', lowBound=0, cat='Continuous') for n in range(N)]
x = [pulp.LpVariable(f'x_{n}', lowBound=0, upBound=C, cat='Continuous') for n in range(N)]

# Objective Function
problem += pulp.lpSum(p[n] * s[n] - c[n] * b[n] - h * x[n] for n in range(N))

# Constraints

# Stock balance and initial/final conditions
problem += (x[0] == 0)
for n in range(N):
    if n == 0:
        problem += (x[n] == b[n] - s[n])
    else:
        problem += (x[n] == x[n-1] + b[n] - s[n])

problem += (x[N-1] == 0)

# Solve the problem
problem.solve()

# Outputs
buyquantity = [pulp.value(bn) for bn in b]
sellquantity = [pulp.value(sn) for sn in s]
stock = [pulp.value(xn) for xn in x]

print("Buy Quantity:", buyquantity)
print("Sell Quantity:", sellquantity)
print("Stock:", stock)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')