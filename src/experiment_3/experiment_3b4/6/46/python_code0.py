import pulp

# Parse the data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7],
}

# Indices
A = len(data['available'])
S = len(data['steel_prices'])

# Problem
problem = pulp.LpProblem("SteelProductionOptimization", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0)

# Objective Function
problem += (
    pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) -
    pulp.lpSum(data['alloy_prices'][a] * alloy_amount[(a, s)] for a in range(A) for s in range(S))
)

# Constraints
# Constraint 1: Alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[(a, s)] for s in range(S)) <= data['available'][a]

# Constraint 2: Total steel production matches the alloy usage
for s in range(S):
    problem += pulp.lpSum(alloy_amount[(a, s)] for a in range(A)) == total_steel[s]

# Constraint 3: Minimum carbon content
for s in range(S):
    problem += (
        pulp.lpSum(data['carbon'][a] * alloy_amount[(a, s)] for a in range(A)) >=
        data['carbon_min'][s] * total_steel[s]
    )

# Constraint 4: Maximum nickel content
for s in range(S):
    problem += (
        pulp.lpSum(data['nickel'][a] * alloy_amount[(a, s)] for a in range(A)) <=
        data['nickel_max'][s] * total_steel[s]
    )

# Constraint 5: Alloy 1 usage constraint
for s in range(S):
    problem += alloy_amount[(0, s)] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')