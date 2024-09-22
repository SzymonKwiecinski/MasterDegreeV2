import pulp

# Data from JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
C = data['capacity']
H = data['holding_cost']
P = data['price']
C_cost = data['cost']
N = len(P)

# Create the problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("Buy", range(1, N + 1), lowBound=0, cat='Continuous')  # Buy quantities
s = pulp.LpVariable.dicts("Sell", range(1, N + 1), lowBound=0, cat='Continuous') # Sell quantities
x = pulp.LpVariable.dicts("Stock", range(1, N + 1), lowBound=0, upBound=C, cat='Continuous') # Stock levels

# Objective Function
problem += pulp.lpSum(P[n-1] * s[n] - C_cost[n-1] * b[n] - H * x[n] for n in range(1, N + 1))

# Constraints
problem += x[1] == b[1] - s[1]  # Initial stock constraint
for n in range(2, N + 1):
    problem += x[n] == x[n-1] + b[n] - s[n]  # Stock balance
problem += x[N] == 0  # Final stock must be zero

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')