import pulp

# Extract data from JSON
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)
S = len(steel_prices)

# Define the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Define the decision variables
alloy_amount = pulp.LpVariable.dicts(
    "alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0
)

total_steel = pulp.LpVariable.dicts(
    "total_steel", (s for s in range(S)), lowBound=0
)

# Objective function: Maximize profit
problem += (
    pulp.lpSum(steel_prices[s] * total_steel[s] for s in range(S))
    - pulp.lpSum(alloy_prices[a] * alloy_amount[(a, s)] for a in range(A) for s in range(S))
)

# Constraints

# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[(a, s)] for s in range(S)) <= available[a]

# Carbon content constraints
for s in range(S):
    problem += pulp.lpSum(carbon[a] * alloy_amount[(a, s)] for a in range(A)) >= carbon_min[s] * total_steel[s]

# Nickel content constraints
for s in range(S):
    problem += pulp.lpSum(nickel[a] * alloy_amount[(a, s)] for a in range(A)) <= nickel_max[s] * total_steel[s]

# Production of each type of steel
for s in range(S):
    problem += total_steel[s] == pulp.lpSum(alloy_amount[(a, s)] for a in range(A))

# Maximum 40% of alloy 1 in each type of steel
for s in range(S):
    problem += alloy_amount[(0, s)] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Prepare the output
alloy_use = [[pulp.value(alloy_amount[(a, s)]) for a in range(A)] for s in range(S)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')