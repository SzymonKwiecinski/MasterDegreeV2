import pulp

# Data from JSON format
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Create a linear programming problem
problem = pulp.LpProblem("WarehouseOperation", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("BuyQuantity", range(1, N + 1), lowBound=0)  # b_n
s = pulp.LpVariable.dicts("SellQuantity", range(1, N + 1), lowBound=0)  # s_n
x = pulp.LpVariable.dicts("Stock", range(1, N + 1), lowBound=0, upBound=C)  # x_n

# Objective function: Maximize profit
problem += pulp.lpSum(p[n - 1] * s[n] - c[n - 1] * b[n] - h * x[n] for n in range(1, N + 1))

# Constraints
problem += (x[1] == b[1] - s[1])  # x_1 = b_1 - s_1
for n in range(2, N + 1):
    problem += (x[n] == x[n - 1] + b[n] - s[n])  # x_n = x_{n-1} + b_n - s_n

for n in range(1, N + 1):
    problem += (x[n] <= C)  # x_n <= C
    problem += (s[n] <= x[n])  # s_n <= x_n

problem += (x[N] == 0)  # x_N = 0

# Solve the problem
problem.solve()

# Output results
buyquantity = [b[n].varValue for n in range(1, N + 1)]
sellquantity = [s[n].varValue for n in range(1, N + 1)]
stock = [x[n].varValue for n in range(1, N + 1)]

print(f'Buy Quantity: {buyquantity}')
print(f'Sell Quantity: {sellquantity}')
print(f'Stock: {stock}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')