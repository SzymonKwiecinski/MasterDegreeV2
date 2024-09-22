import pulp

# Parse input data
data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}

available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steel types

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_use = [[pulp.LpVariable(f'alloy_use_{a}_{s}', lowBound=0) for a in range(A)] for s in range(S)]

# Total steel produced for each type
total_steel = [pulp.LpVariable(f'total_steel_{s}', lowBound=0) for s in range(S)]

# Objective function: Maximize profit
total_profit = pulp.lpSum(steel_prices[s] * total_steel[s] for s in range(S)) - pulp.lpSum(alloy_prices[a] * alloy_use[s][a] for s in range(S) for a in range(A))
problem += total_profit

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_use[s][a] for s in range(S)) <= available[a], f"Alloy_Availability_{a}"

# Alloy usage in steel
for s in range(S):
    problem += pulp.lpSum(alloy_use[s][a] for a in range(A)) == total_steel[s], f"Steel_Production_{s}"

# Carbon content constraints
for s in range(S):
    problem += pulp.lpSum(alloy_use[s][a] * carbon[a] for a in range(A)) >= carbon_min[s] * total_steel[s], f"Carbon_Content_{s}"

# Nickel content constraints
for s in range(S):
    problem += pulp.lpSum(alloy_use[s][a] * nickel[a] for a in range(A)) <= nickel_max[s] * total_steel[s], f"Nickel_Content_{s}"

# Alloy 1 maximum usage constraint
for s in range(S):
    problem += alloy_use[s][0] <= 0.4 * total_steel[s], f"Alloy1_Restriction_{s}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "alloy_use": [[pulp.value(alloy_use[s][a]) for a in range(A)] for s in range(S)],
    "total_steel": [pulp.value(total_steel[s]) for s in range(S)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')