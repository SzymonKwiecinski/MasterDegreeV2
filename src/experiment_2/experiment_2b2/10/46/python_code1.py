import pulp

# Parse the input data
data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)
S = len(steel_prices)

# Create a LP maximization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_amounts = [[pulp.LpVariable(f"alloy_amount_{a}_{s}", lowBound=0, cat='Continuous') for a in range(A)] for s in range(S)]

# Total steel produced of each type
total_steel = [pulp.LpVariable(f"total_steel_{s}", lowBound=0, cat='Continuous') for s in range(S)]

# Auxiliary variables for carbon and nickel contributions
carbon_contribution = [pulp.LpVariable(f"carbon_contribution_{s}", lowBound=0, cat='Continuous') for s in range(S)]
nickel_contribution = [pulp.LpVariable(f"nickel_contribution_{s}", lowBound=0, cat='Continuous') for s in range(S)]

# Objective function
profit = pulp.lpSum([
    steel_prices[s] * total_steel[s] - pulp.lpSum([alloy_prices[a] * alloy_amounts[s][a] for a in range(A)])
    for s in range(S)
])
problem += profit

# Constraints

# Alloy availability constraints
for a in range(A):
    problem += (pulp.lpSum([alloy_amounts[s][a] for s in range(S)]) <= available[a]), f"Alloy_Availability_{a}"

# Carbon percentage constraints
for s in range(S):
    problem += (carbon_contribution[s] >= carbon_min[s] * total_steel[s]), f"Carbon_Minimum_{s}"

# Nickel percentage constraints
for s in range(S):
    problem += (nickel_contribution[s] <= nickel_max[s] * total_steel[s]), f"Nickel_Maximum_{s}"

# Define carbon and nickel contributions
for s in range(S):
    problem += (carbon_contribution[s] == pulp.lpSum([carbon[a] * alloy_amounts[s][a] for a in range(A)])), f"Carbon_Contribution_{s}"
    problem += (nickel_contribution[s] == pulp.lpSum([nickel[a] * alloy_amounts[s][a] for a in range(A)])), f"Nickel_Contribution_{s}"

# Alloy 1 maximum usage constraint (at most 40%)
for s in range(S):
    problem += (alloy_amounts[s][0] <= 0.4 * total_steel[s]), f"Alloy_1_Maximum_{s}"

# Linking total steel with its components
for s in range(S):
    problem += (total_steel[s] == pulp.lpSum([alloy_amounts[s][a] for a in range(A)])), f"Total_Steel_{s}"

# Solve the problem
problem.solve()

# Output the results
result = {
    "alloy_use": [[pulp.value(alloy_amounts[s][a]) for a in range(A)] for s in range(S)],
    "total_steel": [pulp.value(total_steel[s]) for s in range(S)],
    "total_profit": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')