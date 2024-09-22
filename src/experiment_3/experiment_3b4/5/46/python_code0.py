import pulp

# Data from JSON
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Indices
A = len(data['available']) # Number of alloys
S = len(data['steel_prices']) # Number of steels

# Define the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (s for s in range(S)), lowBound=0, cat='Continuous')

# Objective function
objective = pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - \
            pulp.lpSum(data['alloy_prices'][a] * x[a, s] for a in range(A) for s in range(S))
problem += objective

# Constraints
# Availability constraints
for a in range(A):
    problem += pulp.lpSum(x[a, s] for s in range(S)) <= data['available'][a]

# Carbon content constraints
for s in range(S):
    problem += pulp.lpSum(data['carbon'][a] * x[a, s] for a in range(A)) >= data['carbon_min'][s] * y[s]

# Nickel content constraints
for s in range(S):
    problem += pulp.lpSum(data['nickel'][a] * x[a, s] for a in range(A)) <= data['nickel_max'][s] * y[s]

# Steel production balance
for s in range(S):
    problem += pulp.lpSum(x[a, s] for a in range(A)) == y[s]

# Specific alloy usage constraint
for s in range(S):
    problem += x[0, s] <= 0.4 * y[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')