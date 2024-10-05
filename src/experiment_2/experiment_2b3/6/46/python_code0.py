import pulp

# Input data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Extracting parameters
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steels

# Define the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision variables
alloy_use = [[pulp.LpVariable(f"alloy_use_{a}_{s}", lowBound=0) for a in range(A)] for s in range(S)]

# Total steel produced for each type
total_steel = [pulp.lpSum(alloy_use[s][a] for a in range(A)) for s in range(S)]

# Objective Function: Maximize total profit
profit = pulp.lpSum(
    total_steel[s] * steel_prices[s] - pulp.lpSum(alloy_use[s][a] * alloy_prices[a] for a in range(A)) 
    for s in range(S)
)
problem += profit

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_use[s][a] for s in range(S)) <= available[a]

# Minimum carbon content constraints for each steel type
for s in range(S):
    problem += pulp.lpSum(alloy_use[s][a] * carbon[a] for a in range(A)) >= carbon_min[s] * total_steel[s]

# Maximum nickel content constraints for each steel type
for s in range(S):
    problem += pulp.lpSum(alloy_use[s][a] * nickel[a] for a in range(A)) <= nickel_max[s] * total_steel[s]

# Maximum 40% of steel can be made from alloy 1
for s in range(S):
    problem += alloy_use[s][0] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Prepare output data
output = {
    "alloy_use": [[pulp.value(alloy_use[s][a]) for a in range(A)] for s in range(S)],
    "total_steel": [pulp.value(total_steel[s]) for s in range(S)],
    "total_profit": pulp.value(profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')