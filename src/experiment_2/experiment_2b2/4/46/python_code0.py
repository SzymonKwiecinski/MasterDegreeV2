import pulp

# Parse the input data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0)

# Objective function: maximize profit
profit = pulp.lpSum(
    [
        total_steel[s] * steel_prices[s] -
        pulp.lpSum(alloy_amount[a, s] * alloy_prices[a] for a in range(A))
        for s in range(S)
    ]
)
problem += profit

# Add constraints
# 1. Ensure that alloy usage does not exceed availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= available[a]

# 2. Calculate total steel production and ensure balance
for s in range(S):
    problem += total_steel[s] == pulp.lpSum(alloy_amount[a, s] for a in range(A))
    
# 3. Carbon content requirement
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a, s] * carbon[a] for a in range(A)) >= carbon_min[s] * total_steel[s]
    
# 4. Nickel content requirement
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a, s] * nickel[a] for a in range(A)) <= nickel_max[s] * total_steel[s]

# 5. Limit alloy 1 usage to at most 40% of any steel type
for s in range(S):
    problem += alloy_amount[0, s] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Generate output
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_prod = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_prod,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')