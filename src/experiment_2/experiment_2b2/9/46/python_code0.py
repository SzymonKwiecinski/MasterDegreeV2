from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus

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

# Create the optimization problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision Variables
alloy_use = [[LpVariable(f"alloy_amount_{a+1}_{s+1}", lowBound=0) for a in range(A)] for s in range(S)]
total_steel = [LpVariable(f"total_steel_{s+1}", lowBound=0) for s in range(S)]

# Objective Function: Maximize total profit
problem += lpSum(
    (steel_prices[s] * total_steel[s] -
     lpSum(alloy_prices[a] * alloy_use[s][a] for a in range(A)))
    for s in range(S)
)

# Constraints
# 1. The total amount of each alloy used cannot exceed its availability
for a in range(A):
    problem += lpSum(alloy_use[s][a] for s in range(S)) <= available[a]

# 2. Each type of steel must have a minimum percentage of carbon
for s in range(S):
    problem += lpSum(carbon[a] * alloy_use[s][a] for a in range(A)) >= carbon_min[s] * total_steel[s]

# 3. Each type of steel must have a maximum allowable percentage for nickel
for s in range(S):
    problem += lpSum(nickel[a] * alloy_use[s][a] for a in range(A)) <= nickel_max[s] * total_steel[s]

# 4. All steel must have at most 40% of alloy 1
for s in range(S):
    problem += alloy_use[s][0] <= 0.4 * total_steel[s]

# 5. Total steel produced is the sum of the alloys used
for s in range(S):
    problem += lpSum(alloy_use[s][a] for a in range(A)) == total_steel[s]

# Solve the problem
problem.solve()

# Prepare the output
alloy_use_values = [[alloy_use[s][a].varValue for a in range(A)] for s in range(S)]
total_steel_values = [total_steel[s].varValue for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use_values,
    "total_steel": total_steel_values,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')