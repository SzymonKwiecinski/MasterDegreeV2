import pulp

# Read data from JSON format
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Extracting data
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)
S = len(steel_prices)

# Problem
problem = pulp.LpProblem("Steel_Production_Max_Profit", pulp.LpMaximize)

# Decision Variables
alloy_use = [[pulp.LpVariable(f"alloy_use_{a+1}_{s+1}", lowBound=0) for a in range(A)] for s in range(S)]
total_steel = [pulp.LpVariable(f"total_steel_{s+1}", lowBound=0) for s in range(S)]

# Objective Function
total_profit = pulp.lpSum(
    steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_prices[a] * alloy_use[s][a] for a in range(A))
    for s in range(S)
)
problem += total_profit

# Constraints

# Alloy amount constraints
for a in range(A):
    problem += pulp.lpSum(alloy_use[s][a] for s in range(S)) <= available[a], f"Alloy_{a+1}_Availability"

# Composition constraints
for s in range(S):
    problem += pulp.lpSum(alloy_use[s][a] for a in range(A)) == total_steel[s], f"Steel_{s+1}_Production"

    total_carbon = pulp.lpSum(carbon[a] * alloy_use[s][a] for a in range(A))
    problem += total_carbon >= carbon_min[s] * total_steel[s], f"Carbon_Min_Steel_{s+1}"

    total_nickel = pulp.lpSum(nickel[a] * alloy_use[s][a] for a in range(A))
    problem += total_nickel <= nickel_max[s] * total_steel[s], f"Nickel_Max_Steel_{s+1}"

# Alloy 1 constraint
for s in range(S):
    problem += alloy_use[s][0] <= 0.4 * total_steel[s], f"Alloy_1_Limit_Steel_{s+1}"

# Solve the problem
problem.solve()

# Extract results
result = {
    "alloy_use": [[pulp.value(alloy_use[s][a]) for a in range(A)] for s in range(S)],
    "total_steel": [pulp.value(total_steel[s]) for s in range(S)],
    "total_profit": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')