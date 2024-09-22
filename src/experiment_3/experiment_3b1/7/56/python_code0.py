import pulp
import json

# Given data in JSON format
data = '''
{
    "west_time": [[3.5, 4.5], [4, 4], [5, 4]],
    "north_time": [[10, 10, 9], [9, 9, 12]]
}
'''

# Load data
data = json.loads(data)
west_time = data['west_time']
north_time = data['north_time']

# Parameters
N = len(north_time) + 1  # Number of streets (north direction)
W = len(west_time[0]) + 1 # Number of avenues (west direction)

# Create the problem
problem = pulp.LpProblem("Optimal Delivery Path", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum(west_time[n-1][w-1] * x[(n, w)] + north_time[n-1][w-1] * x[(n, w)] 
                       for n in range(1, N) for w in range(1, W))

# Constraints
# Starting point
problem += pulp.lpSum(x[(1, w)] for w in range(1, W)) == 1

# Ending point
problem += pulp.lpSum(x[(N-1, w)] for w in range(1, W)) == 1

# Flow conservation constraints
for n in range(2, N):
    for w in range(2, W):
        problem += x[(n, w)] <= x[(n-1, w)] + x[(n, w-1)]

# Solve the problem
problem.solve()

# Retrieve results
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[(n, w)]) == 1]
total_time = pulp.value(problem.objective)

# Output the results
print(f' (Paths): <PATHS>{paths}</PATHS>')
print(f' (Total Time): <TOTAL_TIME>{total_time}</TOTAL_TIME>')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')