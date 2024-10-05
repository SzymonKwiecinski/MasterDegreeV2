import pulp

# Given data
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

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
alloy_use = [[pulp.LpVariable(f"alloy_amount_{a}_{s}", lowBound=0) for a in range(A)] for s in range(S)]
total_steel = [pulp.LpVariable(f"total_steel_{s}", lowBound=0) for s in range(S)]

# Objective Function
total_revenue = pulp.lpSum(total_steel[s] * steel_prices[s] for s in range(S))
total_cost = pulp.lpSum(alloy_use[s][a] * alloy_prices[a] for s in range(S) for a in range(A))
problem += total_revenue - total_cost, "Total Profit"

# Constraints

# Alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_use[s][a] for s in range(S)) <= available[a], f"Available_alloy_{a}"

# Steel production formulas
for s in range(S):
    problem += pulp.lpSum(alloy_use[s][a] for a in range(A)) == total_steel[s], f"Total_steel_{s}"

# Carbon content constraints
for s in range(S):
    problem += (pulp.lpSum(alloy_use[s][a] * carbon[a] for a in range(A)) >= total_steel[s] * carbon_min[s]), f"Carbon_min_{s}"

# Nickel content constraints
for s in range(S):
    problem += (pulp.lpSum(alloy_use[s][a] * nickel[a] for a in range(A)) <= total_steel[s] * nickel_max[s]), f"Nickel_max_{s}"

# Max 40% of alloy 1 in each type of steel
for s in range(S):
    problem += alloy_use[s][0] <= 0.4 * total_steel[s], f"Max_40_percent_alloy1_steel_{s}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "alloy_use": [[pulp.value(alloy_use[s][a]) for a in range(A)] for s in range(S)],
    "total_steel": [pulp.value(total_steel[s]) for s in range(S)],
    "total_profit": pulp.value(total_revenue - total_cost)
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')