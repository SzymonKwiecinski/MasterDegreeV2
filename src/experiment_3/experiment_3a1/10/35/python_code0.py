import pulp
import json

# Data from JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])  # Number of periods
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']

# Create a linear programming problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("Buy", range(N), lowBound=0)  # quantity bought in each period
s = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)  # quantity sold in each period
x = pulp.LpVariable.dicts("Stock", range(N), lowBound=0)  # stock at the end of each period

# Objective function
profit = pulp.lpSum([p[n] * s[n] - c[n] * b[n] - h * x[n] for n in range(N)])
problem += profit

# Capacity constraints and stock calculation
constraints = []
# Initial condition
problem += (x[0] == 0)  # The warehouse starts empty
# Capacity constraints
for n in range(N):
    if n > 0:  # stock calculation for periods > 1
        problem += (x[n] == x[n-1] + b[n] - s[n])
    else:  # first period
        problem += (x[n] == 0 + b[n] - s[n])
    problem += (x[n] <= C)  # stock must not exceed capacity

# Final condition
problem += (x[N-1] == 0)  # The warehouse must be empty at the end of the last period

# Solve the problem
problem.solve()

# Output result
result = {
    "buyquantity": [b[n].value() for n in range(N)],
    "sellquantity": [s[n].value() for n in range(N)],
    "stock": [x[n].value() for n in range(N)]
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')