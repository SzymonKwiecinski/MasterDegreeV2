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

# Problem
problem = pulp.LpProblem("Steel_Max_Profit", pulp.LpMaximize)

# Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) - \
           pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a, s] for a in range(A) for s in range(S))

# Constraints

# Material availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= data['available'][a]

# Carbon composition constraints
for s in range(S):
    problem += pulp.lpSum(data['carbon'][a] * alloy_amount[a, s] for a in range(A)) >= data['carbon_min'][s] * total_steel[s]

# Nickel composition constraints
for s in range(S):
    problem += pulp.lpSum(data['nickel'][a] * alloy_amount[a, s] for a in range(A)) <= data['nickel_max'][s] * total_steel[s]

# Alloy type 1 restriction
for s in range(S):
    problem += pulp.lpSum(alloy_amount[0, s] for s in range(S)) <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Print the objective
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')