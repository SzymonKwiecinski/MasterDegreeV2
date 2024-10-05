import pulp

# Data from JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Problem setup
N = len(data['demand'])
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{n}', lowBound=0) for n in range(N)]
y = [pulp.LpVariable(f'y_{n}', lowBound=0) for n in range(N)]
s = [pulp.LpVariable(f's_{n}', lowBound=0) for n in range(N + 1)]

# Objective function
problem += pulp.lpSum([
    data['cost_regular'] * x[n] + 
    data['cost_overtime'] * y[n] + 
    data['store_cost'] * s[n] 
    for n in range(N)
])

# Constraints
s[0] = 0  # Initial stock
for n in range(N):
    problem += x[n] + y[n] + s[n] - s[n+1] == data['demand'][n]
    problem += x[n] <= data['max_regular_amount']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')