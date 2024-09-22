import pulp

# Problem data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Extract data
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  # number of alloys
S = len(steel_prices)  # number of steel types

# Initialize problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("AlloyAmount", [(a, s) for a in range(A) for s in range(S)], lowBound=0)

# Objective function
profit = pulp.lpSum(
    (steel_prices[s] * pulp.lpSum(alloy_amount[a, s] for a in range(A)) 
     - pulp.lpSum(alloy_prices[a] * alloy_amount[a, s] for a in range(A)))
    for s in range(S)
)
problem += profit, "Total Profit"

# Constraints

# Alloy usage restriction
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= available[a], f"AlloyAvailability_{a}"

# Carbon content requirement
for s in range(S):
    problem += (pulp.lpSum(carbon[a] * alloy_amount[a, s] for a in range(A))
                >= carbon_min[s] * pulp.lpSum(alloy_amount[a, s] for a in range(A))), f"CarbonContent_{s}"

# Nickel content restriction
for s in range(S):
    problem += (pulp.lpSum(nickel[a] * alloy_amount[a, s] for a in range(A))
                <= nickel_max[s] * pulp.lpSum(alloy_amount[a, s] for a in range(A))), f"NickelContent_{s}"

# Alloy 1 limitation
for s in range(S):
    problem += alloy_amount[0, s] <= 0.4 * pulp.lpSum(alloy_amount[a, s] for a in range(A)), f"Alloy1_Limit_{s}"

# Solve the problem
problem.solve()

# Prepare the output
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel = [sum(alloy_use[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')