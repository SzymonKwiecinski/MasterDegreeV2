import pulp

# Data from the problem
data = {
    "available": [40, 50, 80],
    "carbon": [3, 4, 3.5],
    "nickel": [1, 1.5, 1.8],
    "alloy_prices": [380, 400, 440],
    "steel_prices": [650, 600],
    "carbon_min": [3.6, 3.4],
    "nickel_max": [1.5, 1.7]
}

# A is the number of alloys, S is the number of steel types
A = len(data['available'])
S = len(data['steel_prices'])

# Create a problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_use = [[pulp.LpVariable(f'alloy_use_{a}_{s}', lowBound=0) for a in range(A)] for s in range(S)]
total_steel = [pulp.LpVariable(f'total_steel_{s}', lowBound=0) for s in range(S)]

# Objective function: Maximize total profit
profit = pulp.lpSum(
    data['steel_prices'][s]*total_steel[s] - pulp.lpSum(data['alloy_prices'][a]*alloy_use[s][a] for a in range(A))
    for s in range(S)
)
problem += profit

# Constraints

# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_use[s][a] for s in range(S)) <= data['available'][a]

# Steel production constraints
for s in range(S):
    problem += pulp.lpSum(alloy_use[s][a] for a in range(A)) == total_steel[s]

# Minimum carbon percentage constraints
for s in range(S):
    problem += (pulp.lpSum(data['carbon'][a]*alloy_use[s][a] for a in range(A)) >=
                data['carbon_min'][s] * total_steel[s])

# Maximum nickel percentage constraints
for s in range(S):
    problem += (pulp.lpSum(data['nickel'][a]*alloy_use[s][a] for a in range(A)) <=
                data['nickel_max'][s] * total_steel[s])

# At most 40% of alloy 1 constraint
for s in range(S):
    problem += alloy_use[s][0] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Collect results
alloy_use_solution = [[pulp.value(alloy_use[s][a]) for a in range(A)] for s in range(S)]
total_steel_solution = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "alloy_use": alloy_use_solution,
    "total_steel": total_steel_solution,
    "total_profit": total_profit
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')