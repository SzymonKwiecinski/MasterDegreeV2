import pulp

# Data from JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)  # Number of periods

# Create a problem variable
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Variables
b = [pulp.LpVariable(f'b_{n}', lowBound=0, cat='Continuous') for n in range(N)]
s = [pulp.LpVariable(f's_{n}', lowBound=0, cat='Continuous') for n in range(N)]
x = [pulp.LpVariable(f'x_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Objective function to maximize profit
profit_terms = [(p[n] * s[n] - c[n] * b[n] - h * x[n]) for n in range(N)]
problem += pulp.lpSum(profit_terms)

# Constraints
# Initial stock condition
problem += x[0] == 0  # x_0 = 0

# Stock balance and capacity constraints for each period
for n in range(N):
    if n > 0:
        problem += x[n] == x[n-1] + b[n] - s[n]  # Stock balance
    problem += x[n] <= C  # Capacity

# Final stock condition
problem += x[N-1] == 0  # x_N = 0

# Solve the problem
problem.solve()

# Output results
buy_quantity = [pulp.value(b[n]) for n in range(N)]
sell_quantity = [pulp.value(s[n]) for n in range(N)]
stock = [pulp.value(x[n]) for n in range(N)]

print("Buy quantity:", buy_quantity)
print("Sell quantity:", sell_quantity)
print("Stock:", stock)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')