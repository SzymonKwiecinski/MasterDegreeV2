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

# Parameters
A = len(data['available'])
S = len(data['steel_prices'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat=pulp.LpContinuous)

# Objective Function
revenue = pulp.lpSum(data['steel_prices'][s] * pulp.lpSum(x[a, s] for a in range(A)) for s in range(S))
costs = pulp.lpSum(data['alloy_prices'][a] * x[a, s] for a in range(A) for s in range(S))
problem += revenue - costs

# Constraints

# Alloy Availability Constraints
for a in range(A):
    problem += pulp.lpSum(x[a, s] for s in range(S)) <= data['available'][a]

# Carbon Content Constraints
for s in range(S):
    problem += pulp.lpSum(data['carbon'][a] * x[a, s] for a in range(A)) >= data['carbon_min'][s] * pulp.lpSum(x[a, s] for a in range(A))

# Nickel Content Constraints
for s in range(S):
    problem += pulp.lpSum(data['nickel'][a] * x[a, s] for a in range(A)) <= data['nickel_max'][s] * pulp.lpSum(x[a, s] for a in range(A))

# Alloy 1 Usage Constraint
for s in range(S):
    problem += x[0, s] <= 0.4 * pulp.lpSum(x[a, s] for a in range(A))

# Solve the problem
problem.solve()

# Results
solution = {(a, s): x[a, s].varValue for a in range(A) for s in range(S)}

print(f"Amount of each alloy used in each type of steel: {solution}")
for s in range(S):
    steel_total = sum(x[a, s].varValue for a in range(A))
    print(f"Total amount of steel type {s}: {steel_total}")

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')