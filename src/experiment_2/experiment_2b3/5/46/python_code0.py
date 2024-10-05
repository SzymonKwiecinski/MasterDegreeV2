import pulp

# Data input
data = {
    "available": [40, 50, 80],
    "carbon": [3, 4, 3.5],
    "nickel": [1, 1.5, 1.8],
    "alloy_prices": [380, 400, 440],
    "steel_prices": [650, 600],
    "carbon_min": [3.6, 3.4],
    "nickel_max": [1.5, 1.7]
}

available = data["available"]
carbon = data["carbon"]
nickel = data["nickel"]
alloy_prices = data["alloy_prices"]
steel_prices = data["steel_prices"]
carbon_min = data["carbon_min"]
nickel_max = data["nickel_max"]

A = len(available)
S = len(steel_prices)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", [(a, s) for a in range(A) for s in range(S)], lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", [s for s in range(S)], lowBound=0, cat='Continuous')

# Objective Function
total_revenue = pulp.lpSum([steel_prices[s] * total_steel[s] for s in range(S)])
total_cost = pulp.lpSum([alloy_prices[a] * alloy_amount[(a, s)] for a in range(A) for s in range(S)])
problem += total_revenue - total_cost

# Constraints
# Availability constraints
for a in range(A):
    problem += pulp.lpSum([alloy_amount[(a, s)] for s in range(S)]) <= available[a], f"Availability_{a}"

# Carbon percentage constraints
for s in range(S):
    problem += pulp.lpSum([carbon[a] * alloy_amount[(a, s)] for a in range(A)]) >= carbon_min[s] * total_steel[s], f"Carbon_min_{s}"

# Nickel percentage constraints
for s in range(S):
    problem += pulp.lpSum([nickel[a] * alloy_amount[(a, s)] for a in range(A)]) <= nickel_max[s] * total_steel[s], f"Nickel_max_{s}"

# Alloy 1 usage constraint
for s in range(S):
    problem += alloy_amount[(0, s)] <= 0.4 * total_steel[s], f"Alloy1_usage_{s}"

# Total steel production constraint
for s in range(S):
    problem += pulp.lpSum([alloy_amount[(a, s)] for a in range(A)]) == total_steel[s], f"Total_steel_{s}"

# Solve
problem.solve()

# Output
alloy_use = [[pulp.value(alloy_amount[(a, s)]) for a in range(A)] for s in range(S)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_produced,
    "total_profit": total_profit
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')