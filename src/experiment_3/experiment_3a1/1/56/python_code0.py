import pulp
import json

# Input data
data = json.loads("{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}")
west_time = data['west_time']
north_time = data['north_time']

# Parameters
N = len(north_time) + 1  # Number of streets (rows)
W = len(west_time[0]) + 1  # Number of avenues (columns)

# Create the LP problem
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum(west_time[n-1][w-1] * x[n, w] + north_time[n-1][w-1] * x[n, w] 
                      for n in range(1, N) for w in range(1, W)), "TotalWalkingTime"

# Constraints
# Flow Conservation
for n in range(1, N):
    problem += pulp.lpSum(x[n, w] for w in range(1, W)) == 1

# Path Activation
for w in range(1, W):
    problem += pulp.lpSum(x[n, w] for n in range(1, N)) == 1

# Starting Point
problem += x[1, 1] == 1, "StartPoint"

# Ending Point
problem += x[N-1, W-1] == 1, "EndPoint"

# Solve the problem
problem.solve()

# Output the results
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[n, w]) == 1]
total_time = pulp.value(problem.objective)

print(f'Paths: {paths}')
print(f'Total Time: {total_time}')
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')