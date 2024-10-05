import pulp

# Input data
data = {
    "large_roll_width": 70,
    "demands": [40, 65, 80, 75],
    "roll_width_options": [17, 14, 11, 8.5],
    "patterns": [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]
}

# Problem data
large_roll_width = data["large_roll_width"]
demands = data["demands"]
patterns = data["patterns"]

# Number of pattern and demand types
N = len(patterns)
M = len(demands)

# Create the MILP model
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', cat='Integer', lowBound=0) for i in range(N)]

# Objective function: Minimize the total number of large rolls required
problem += pulp.lpSum(x), "Total Large Rolls"

# Constraints: Ensure demands are met for each roll width option
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j], f'Demand_Constraint_{j}'

# Solve the optimization problem
problem.solve()

# Extract the results
patterns_result = [{
    "pattern": patterns[i],
    "amount": int(x[i].varValue)
} for i in range(N) if x[i].varValue > 0]

total_large_rolls_used = sum(int(x[i].varValue) for i in range(N))

# Output results
output = {
    "patterns": patterns_result,
    "total_large_rolls_used": total_large_rolls_used
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')