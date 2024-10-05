import pulp

# Load data
data = {
    "available": [40, 50, 80],
    "carbon": [3, 4, 3.5],
    "nickel": [1, 1.5, 1.8],
    "alloy_prices": [380, 400, 440],
    "steel_prices": [650, 600],
    "carbon_min": [3.6, 3.4],
    "nickel_max": [1.5, 1.7]
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

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_use = pulp.LpVariable.dicts("AlloyUse", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("TotalSteel", (s for s in range(S)), lowBound=0)

# Objective function
profit = pulp.lpSum(
    steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_prices[a] * alloy_use[a, s] for a in range(A))
    for s in range(S)
)
problem += profit

# Constraints
# 1. Availability of each alloy
for a in range(A):
    problem += pulp.lpSum(alloy_use[a, s] for s in range(S)) <= available[a]

# 2. Carbon and Nickel requirements for each steel type
for s in range(S):
    # Carbon constraints
    problem += pulp.lpSum(carbon[a] * alloy_use[a, s] for a in range(A)) >= carbon_min[s] * total_steel[s]
    # Nickel constraints
    problem += pulp.lpSum(nickel[a] * alloy_use[a, s] for a in range(A)) <= nickel_max[s] * total_steel[s]

# 3. Alloy 1 usage constraint
for s in range(S):
    problem += alloy_use[0, s] <= 0.4 * total_steel[s]

# 4. Total steel production is the sum of alloys used
for s in range(S):
    problem += total_steel[s] == pulp.lpSum(alloy_use[a, s] for a in range(A))

# Solve the problem
problem.solve()

# Collect results
alloy_use_result = [[pulp.value(alloy_use[a, s]) for a in range(A)] for s in range(S)]
total_steel_result = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use_result,
    "total_steel": total_steel_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')