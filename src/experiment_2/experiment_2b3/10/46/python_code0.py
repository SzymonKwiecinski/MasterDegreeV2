import pulp

# Parse input data
data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 
        'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 
        'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}

available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steel types

# Define the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Variables
alloy_use = pulp.LpVariable.dicts("alloy_use", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0, cat='Continuous')

# Objective function: maximize profit
total_profit = pulp.lpSum([
    steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_prices[a] * alloy_use[a, s] for a in range(A))
    for s in range(S)
])
problem += total_profit

# Constraints
# Alloy availability constraint
for a in range(A):
    problem += pulp.lpSum(alloy_use[a, s] for s in range(S)) <= available[a]

# Material balance constraint for steels
for s in range(S):
    problem += pulp.lpSum(alloy_use[a, s] for a in range(A)) == total_steel[s]

# Carbon percentage constraint
for s in range(S):
    problem += (
        pulp.lpSum(alloy_use[a, s] * carbon[a] for a in range(A)) 
        >= carbon_min[s] * total_steel[s]
    )

# Nickel percentage constraint
for s in range(S):
    problem += (
        pulp.lpSum(alloy_use[a, s] * nickel[a] for a in range(A)) 
        <= nickel_max[s] * total_steel[s]
    )

# Alloy 1 usage constraint
for s in range(S):
    problem += alloy_use[0, s] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Collect results
alloy_use_result = [[alloy_use[a, s].varValue for a in range(A)] for s in range(S)]
total_steel_result = [total_steel[s].varValue for s in range(S)]
total_profit_result = pulp.value(problem.objective)

result = {
    "alloy_use": alloy_use_result,
    "total_steel": total_steel_result,
    "total_profit": total_profit_result
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')