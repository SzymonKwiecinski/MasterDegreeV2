import pulp
import json

# Load data from JSON format
data = json.loads("{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}")
west_time = data['west_time']
north_time = data['north_time']

# Define dimensions
N = len(north_time) + 1  # Number of intersections in the N direction
W = len(west_time[0]) + 1  # Number of intersections in the W direction

# Initialize the problem
problem = pulp.LpProblem("OptimalPathInGrid", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N-1) for w in range(W-1)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(N-1) for w in range(W-1)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(x[n, w] * west_time[n][w] + y[n, w] * north_time[n][w] for n in range(N-1) for w in range(W-1)), "Total Travel Time"

# Constraints
# Constraint for the starting point (1,1)
problem += x[0, 0] + y[0, 0] == 1, "Start_Constraint"

# Constraint for the final intersection (W,N)
problem += x[N-2, W-2] + y[N-2, W-2] == 1, "End_Constraint"

# Movement constraints
for n in range(N-1):
    for w in range(W-1):
        if n > 0:
            problem += x[n-1, w] + y[n, w] <= 1, f"Flow_Constraint_n{n}_w{w}"
        if w > 0:
            problem += x[n, w-1] + y[n, w] <= 1, f"Flow_Constraint_n{n}_w{w}2"

# Solve the problem
problem.solve()

# Print the value of the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')