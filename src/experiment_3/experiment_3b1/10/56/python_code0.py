import pulp
import json

# Data input
data = json.loads("{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}")
west_time = data['west_time']
north_time = data['north_time']

# Define the grid dimensions
N = len(north_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Create the problem
problem = pulp.LpProblem("Delivery_Path_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N) for w in range(W)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(x[n, w] for n in range(N) for w in range(W)), "Total_Travel_Time"

# Constraints
# Destination constraints
problem += x[N-1, W-1] == 0, "Destination_Constraint"

# Movement constraints
for n in range(N):
    for w in range(W-1):  # for west movement
        problem += x[n, w] == west_time[n][w] + x[n, w+1], f"West_Movement_Constraint_{n}_{w}"
        
for n in range(N-1):  # for north movement
    for w in range(W):
        problem += x[n, w] == north_time[n][w] + x[n+1, w], f"North_Movement_Constraint_{n}_{w}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')