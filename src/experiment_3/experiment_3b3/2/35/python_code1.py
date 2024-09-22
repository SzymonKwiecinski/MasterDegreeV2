import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Unpacking data
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

# Problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("Buy", range(1, N + 1), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("Sell", range(1, N + 1), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("Stock", range(1, N + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(p[n-1] * s[n] - c[n-1] * b[n] - h * x[n] for n in range(1, N + 1))

# Constraints
# Remove the initial stock constraint as x[0] does not exist
# Initialize with a constraint for the first stock level
problem += x[1] == b[1] - s[1]

for n in range(1, N + 1):
    if n > 1:
        problem += x[n] == x[n-1] + b[n] - s[n]
    problem += x[n] <= C

problem += x[N] == 0  # Final stock constraint

# Solve
problem.solve()

# Results
buy_quantities = [pulp.value(b[i]) for i in range(1, N + 1)]
sell_quantities = [pulp.value(s[i]) for i in range(1, N + 1)]
stock_levels = [pulp.value(x[i]) for i in range(1, N + 1)]

print("Buy quantities:", buy_quantities)
print("Sell quantities:", sell_quantities)
print("Stock levels:", stock_levels)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')