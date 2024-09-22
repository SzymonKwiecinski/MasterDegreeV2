import pulp

# Data
data = {
    "available": [40, 50, 80],
    "carbon": [3, 4, 3.5],
    "nickel": [1, 1.5, 1.8],
    "alloy_prices": [380, 400, 440],
    "steel_prices": [650, 600],
    "carbon_min": [3.6, 3.4],
    "nickel_max": [1.5, 1.7]
}

A = len(data['available'])
S = len(data['steel_prices'])

# Problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Variables
alloy_use = pulp.LpVariable.dicts("AlloyAmount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("TotalSteel", (s for s in range(S)), lowBound=0)

# Objective
total_profit = pulp.lpSum(
    [data['steel_prices'][s] * total_steel[s] - 
     pulp.lpSum(data['alloy_prices'][a] * alloy_use[a, s] for a in range(A))
     for s in range(S)]
)
problem += total_profit

# Constraints
for a in range(A):
    problem += pulp.lpSum(alloy_use[a, s] for s in range(S)) <= data['available'][a]

for s in range(S):
    problem += pulp.lpSum(alloy_use[a, s] for a in range(A)) == total_steel[s]
    problem += (pulp.lpSum(data['carbon'][a] * alloy_use[a, s] for a in range(A)) >= 
                data['carbon_min'][s] * total_steel[s])
    problem += (pulp.lpSum(data['nickel'][a] * alloy_use[a, s] for a in range(A)) <= 
                data['nickel_max'][s] * total_steel[s])

# Additional constraint for alloy 1
for s in range(S):
    problem += alloy_use[0, s] <= 0.4 * total_steel[s]

# Solve problem
problem.solve()

# Output
alloy_use_result = [[pulp.value(alloy_use[a, s]) for a in range(A)] for s in range(S)]
total_steel_result = [pulp.value(total_steel[s]) for s in range(S)]
total_profit_result = pulp.value(problem.objective)

result = {
    "alloy_use": alloy_use_result,
    "total_steel": total_steel_result,
    "total_profit": total_profit_result
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')