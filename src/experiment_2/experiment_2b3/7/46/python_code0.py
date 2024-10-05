import pulp

# Data loading
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

A = len(available)
S = len(steel_prices)

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_use = [
    [pulp.LpVariable(f"alloy_{a+1}_steel_{s+1}", lowBound=0) for a in range(A)] 
    for s in range(S)
]

total_steel = [pulp.LpVariable(f"total_steel_{s+1}", lowBound=0) for s in range(S)]

# Objective function
problem += pulp.lpSum([
    steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_prices[a] * alloy_use[s][a] for a in range(A))
    for s in range(S)
])

# Constraints
for s in range(S):
    # Total steel produced from alloys constraint
    problem += (pulp.lpSum(alloy_use[s][a] for a in range(A)) == total_steel[s])
    
    # Carbon constraint
    problem += (
        pulp.lpSum(carbon[a] * alloy_use[s][a] for a in range(A)) 
        >= carbon_min[s] * total_steel[s]
    )
    
    # Nickel constraint
    problem += (
        pulp.lpSum(nickel[a] * alloy_use[s][a] for a in range(A)) 
        <= nickel_max[s] * total_steel[s]
    )

# Alloy availability constraints
for a in range(A):
    problem += (
        pulp.lpSum(alloy_use[s][a] for s in range(S)) <= available[a]
    )

# Maximum 40% of alloy 1 constraint
for s in range(S):
    problem += (alloy_use[s][0] <= 0.4 * total_steel[s])

# Solve the problem
problem.solve()

# Prepare the outputs
alloy_use_result = [[pulp.value(alloy_use[s][a]) for a in range(A)] for s in range(S)]
total_steel_result = [pulp.value(total_steel[s]) for s in range(S)]
total_profit_result = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use_result,
    "total_steel": total_steel_result,
    "total_profit": total_profit_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')