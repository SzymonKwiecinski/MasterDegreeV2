import pulp

# Data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create the linear programming problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - \
           pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(x[a, s] for s in range(S)) for a in range(A))

# Constraints
# Alloy availability
for a in range(A):
    problem += pulp.lpSum(x[a, s] for s in range(S)) <= data['available'][a]

# Carbon content
for s in range(S):
    problem += pulp.lpSum(x[a, s] * data['carbon'][a] for a in range(A)) >= data['carbon_min'][s] * y[s]

# Nickel content
for s in range(S):
    problem += pulp.lpSum(x[a, s] * data['nickel'][a] for a in range(A)) <= data['nickel_max'][s] * y[s]

# Alloy 1 restriction
problem += pulp.lpSum(x[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')