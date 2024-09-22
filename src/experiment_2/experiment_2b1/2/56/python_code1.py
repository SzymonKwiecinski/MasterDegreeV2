import pulp
import json

# Load data from the given JSON format
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Define the parameters
west_time = data['west_time']
north_time = data['north_time']
N = len(west_time)  # number of streets (rows)
W = len(west_time[0]) + 1  # number of avenues (columns)

# Create the problem variable
problem = pulp.LpProblem("Delivery_Time_Minimization", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", [(n, w) for n in range(N) for w in range(W)], cat='Binary')

# Objective function: Minimize total travel time
total_travel_time = pulp.lpSum([
    north_time[n][w] * x[(n, w)] if n < N - 1 else 0 
    for n in range(N) for w in range(W)
] + [
    west_time[n][w] * x[(n, w)] if w < W - 1 else 0 
    for n in range(N) for w in range(W)
])

# Set the objective function
problem += total_travel_time

# Constraints

# Start at (0,0)
problem += x[(0, 0)] == 1

# Ensure that each street and avenue is visited exactly once
for n in range(N):
    problem += pulp.lpSum(x[(n, w)] for w in range(W)) <= 1

for w in range(W):
    problem += pulp.lpSum(x[(n, w)] for n in range(N)) <= 1

# Ensure the end point is reached
problem += pulp.lpSum(x[(N-1, w)] for w in range(W)) == 1
problem += pulp.lpSum(x[(n, W-1)] for n in range(N)) == 1

# Solve the problem
problem.solve()

# Prepare output
total_time = pulp.value(problem.objective)
paths = [(n, w) for (n, w) in x.keys() if x[(n, w)].varValue == 1]

# Formulate the output
output = {
    "paths": paths,
    "total_time": total_time
}

# Print the output
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')