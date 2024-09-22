import pulp
import json

# Provided data in JSON format
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

# Extracting the dimensions and time matrices
west_time = data['west_time']
north_time = data['north_time']
N = len(north_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Initialize the linear programming problem
problem = pulp.LpProblem("Delivery_Person_Path", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective function: Minimize total delivery time
problem += pulp.lpSum(
    west_time[n-1][w-1] * x[(n, w)] + north_time[n-1][w-1] * x[(n, w)]
    for n in range(1, N) for w in range(1, W)
), "Total_Delivery_Time"

# Constraints: Delivery person can only move north or west
for w in range(1, W):
    problem += pulp.lpSum(x[(n, w)] for n in range(1, N)) + pulp.lpSum(x[(w, w)] for w in range(1, W)) == 1, f"Movement_Constraint_w{w}")

# Flow conservation constraints
for n in range(1, N):
    for w in range(1, W):
        problem += x[(n, w)] <= pulp.lpSum(x[(n_prime, w)] for n_prime in range(1, N)), f"Flow_Conservation_n{n}_w{w}"

# Solve the problem
problem.solve()

# Collecting results
optimal_paths = [(n, w) for n in range(1, N) for w in range(1, W) if x[(n, w)].value() == 1]
total_travel_time = pulp.value(problem.objective)

# Outputting the result
output = {"paths": optimal_paths, "total_time": total_travel_time}
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')