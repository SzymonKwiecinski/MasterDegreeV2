import pulp
import json

# Given data in JSON format
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Initialize variables
N = len(data['north_time'][0])  # Number of streets (north)
W = len(data['west_time'])       # Number of avenues (west)

# Create the Linear Programming problem
problem = pulp.LpProblem("Travel_Time_Minimization", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N + 1) for w in range(1, W + 1)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['west_time'][w - 1][n - 1] * x[(n, w)] + 
    data['north_time'][n - 1][w - 1] * x[(n, w)]
    for n in range(1, N + 1) for w in range(1, W + 1)
)

# Constraints
# Start at (1,1)
problem += pulp.lpSum(x[(1, w)] for w in range(1, W + 1)) == 1

# End at (W,N)
problem += pulp.lpSum(x[(N, W)]) == 1

# Flow conservation constraints
for n in range(1, N + 1):
    for w in range(1, W + 1):
        problem += pulp.lpSum(x[(n, w)] for w in range(1, W + 1)) - pulp.lpSum(x[(n, w)] for n in range(1, N + 1)) == 0

# Solve the problem
problem.solve()

# Collecting results
total_travel_time = pulp.value(problem.objective)
paths = [(n, w) for (n, w) in x if x[(n, w)].varValue == 1]

# Output results
output = {
    "paths": paths,
    "total_time": total_travel_time
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{total_travel_time}</OBJ>')