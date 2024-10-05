import pulp

# Data provided
data = {
    "large_roll_width": 70, 
    "demands": [40, 65, 80, 75], 
    "roll_width_options": [17, 14, 11, 8.5], 
    "patterns": [
        [4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], 
        [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], 
        [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], 
        [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], 
        [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], 
        [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], 
        [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], 
        [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], 
        [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], 
        [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], 
        [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], 
        [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], 
        [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], 
        [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], 
        [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], 
        [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], 
        [0, 0, 0, 8]
    ]
}

# Extract data
large_roll_width = data["large_roll_width"]
demands = data["demands"]
patterns = data["patterns"]

# Initialize the problem
problem = pulp.LpProblem("Minimize_Large_Roll_Usage", pulp.LpMinimize)

# Define decision variables
N = len(patterns)
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(N)]

# Objective: Minimize the number of large rolls used
problem += pulp.lpSum(x), "Total_Large_Rolls"

# Constraints: Fulfill the demand for each roll width
M = len(demands)
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j], f"Demand_for_{j+1}"

# Solve the problem
problem.solve()

# Collect results
output_patterns = [
    {"pattern": patterns[i], "amount": x[i].varValue} for i in range(N) if x[i].varValue > 0
]
total_large_rolls = pulp.value(problem.objective)

# Format output
output = {
    "patterns": output_patterns,
    "total_large_rolls_used": total_large_rolls
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')