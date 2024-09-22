import pulp

# Given data
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

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_use = pulp.LpVariable.dicts("alloy_use", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')

# Constraints
for a in range(A):
    problem += pulp.lpSum(alloy_use[a, s] for s in range(S)) <= data['available'][a], f"Alloy_Availability_{a}"

for s in range(S):
    total_steel_s = pulp.lpSum(alloy_use[a, s] for a in range(A))
    problem += pulp.lpSum(data['carbon'][a] * alloy_use[a, s] for a in range(A)) >= data['carbon_min'][s] * total_steel_s, f"Carbon_Content_{s}"
    problem += pulp.lpSum(data['nickel'][a] * alloy_use[a, s] for a in range(A)) <= data['nickel_max'][s] * total_steel_s, f"Nickel_Content_{s}"

# Alloy 1 constraint
for s in range(S):
    problem += alloy_use[0, s] <= 0.4 * pulp.lpSum(alloy_use[a, s] for a in range(A)), f"Alloy_1_Limit_{s}"

# Objective function
revenue = pulp.lpSum(data['steel_prices'][s] * pulp.lpSum(alloy_use[a, s] for a in range(A)) for s in range(S))
cost = pulp.lpSum(data['alloy_prices'][a] * alloy_use[a, s] for a in range(A) for s in range(S))
problem += revenue - cost, "Total_Profit"

# Solve the problem
problem.solve()

# Output results
alloy_use_result = [[pulp.value(alloy_use[a, s]) for a in range(A)] for s in range(S)]
total_steel_result = [pulp.value(pulp.lpSum(alloy_use[a, s] for a in range(A))) for s in range(S)]

output = {
    "alloy_use": alloy_use_result,
    "total_steel": total_steel_result,
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')