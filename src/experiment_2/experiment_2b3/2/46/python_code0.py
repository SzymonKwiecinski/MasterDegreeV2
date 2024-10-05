import pulp

# Data from JSON
data = {
    "available": [40, 50, 80],
    "carbon": [3, 4, 3.5],
    "nickel": [1, 1.5, 1.8],
    "alloy_prices": [380, 400, 440],
    "steel_prices": [650, 600],
    "carbon_min": [3.6, 3.4],
    "nickel_max": [1.5, 1.7]
}

# Constants
A = len(data["available"])
S = len(data["steel_prices"])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", [(a, s) for a in range(A) for s in range(S)], lowBound=0)

total_steel = pulp.LpVariable.dicts("total_steel", [s for s in range(S)], lowBound=0)

# Objective: Maximize profit
profit = pulp.lpSum(
    (data["steel_prices"][s] - data["alloy_prices"][a]) * alloy_amount[a, s]
    for a in range(A) for s in range(S)
)
problem += profit

# Constraints

# Alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= data["available"][a]

# Carbon percentage constraint
for s in range(S):
    problem += (pulp.lpSum(alloy_amount[a, s] * data["carbon"][a] for a in range(A)) 
                >= data["carbon_min"][s] * total_steel[s])

# Nickel percentage constraint
for s in range(S):
    problem += (pulp.lpSum(alloy_amount[a, s] * data["nickel"][a] for a in range(A)) 
                <= data["nickel_max"][s] * total_steel[s])

# Alloy 1 limitation (at most 40%)
for s in range(S):
    problem += alloy_amount[0, s] <= 0.4 * total_steel[s]

# Total steel calculation
for s in range(S):
    problem += (total_steel[s] == pulp.lpSum(alloy_amount[a, s] for a in range(A)))

# Solve
problem.solve()

# Results
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(S)]

# Output
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_produced,
    "total_profit": pulp.value(problem.objective)
}

print(output)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')