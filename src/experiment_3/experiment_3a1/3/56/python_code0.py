import pulp
import json

# Define the data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Extract the dimensions
W = len(data['west_time'][0])  # number of avenues
N = len(data['north_time'])      # number of streets

# Create the linear programming problem
problem = pulp.LpProblem("Delivery_Path_Optimization", pulp.LpMinimize)

# Define the decision variables
x = pulp.LpVariable.dicts("north", (range(1, N), range(1, W+1)), lowBound=0, upBound=1, cat='Continuous')
y = pulp.LpVariable.dicts("west", (range(1, N+1), range(1, W)), lowBound=0, upBound=1, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['north_time'][n-1][w-1] * x[n][w] for n in range(1, N) for w in range(1, W+1)) + \
           pulp.lpSum(data['west_time'][n-1][w-1] * y[n][w] for n in range(1, N+1) for w in range(1, W))

# Constraints
# Starting Point Constraint
problem += x[1][1] + y[1][1] == 1

# Flow Conservation Constraints
for n in range(1, N):
    for w in range(1, W+1):
        problem += x[n][w] + y[n][w] == 1

# End Point Constraint
problem += pulp.lpSum(x[N][w] for w in range(1, W+1)) + pulp.lpSum(y[n][W] for n in range(1, N)) == 1

# Solve the problem
problem.solve()

# Prepare the output
total_travel_time = pulp.value(problem.objective)
paths = [(n, w) for n in range(1, N) for w in range(1, W+1) if pulp.value(x[n][w]) > 0] + \
        [(n, W) for n in range(1, N) if pulp.value(y[n][W]) > 0]

output = {
    "paths": paths,
    "total_time": total_travel_time
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_travel_time}</OBJ>')