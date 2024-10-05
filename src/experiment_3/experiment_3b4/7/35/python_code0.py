import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{n}", lowBound=0, cat='Continuous') for n in range(N)]
y = [pulp.LpVariable(f"y_{n}", lowBound=0, cat='Continuous') for n in range(N)]
s = [pulp.LpVariable(f"s_{n}", lowBound=0, cat='Continuous') for n in range(N+1)]

# Set s_0 to 0
problem += (s[0] == 0)

# Objective Function
problem += pulp.lpSum(data['price'][n] * y[n] - data['cost'][n] * x[n] - data['holding_cost'] * s[n+1] for n in range(N))

# Constraints
for n in range(N):
    # Stock balance constraint
    problem += (s[n+1] == s[n] + x[n] - y[n])
    # Capacity constraint
    problem += (s[n+1] <= data['capacity'])

# Final stock condition
problem += (s[N] == 0)

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')