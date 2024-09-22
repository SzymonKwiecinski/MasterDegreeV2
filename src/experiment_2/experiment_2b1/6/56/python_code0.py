import pulp
import json

# Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1  # number of north streets
W = len(west_time[0]) + 1  # number of west avenues

# Create the LP problem
problem = pulp.LpProblem("Delivery_Time_Optimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective Function
problem += pulp.lpSum(x[n, w] * (north_time[n-1][w] if n > 0 else 0) for n in range(N) for w in range(W)) + \
            pulp.lpSum(x[n, w] * (west_time[n][w-1] if w > 0 else 0) for n in range(N) for w in range(W)), "Total_Delivery_Time"

# Constraints
for n in range(N):
    problem += pulp.lpSum(x[n, w] for w in range(W)) == 1  # exactly one path in each row

for w in range(W):
    problem += pulp.lpSum(x[n, w] for n in range(N)) == 1  # exactly one path in each column

# Starting point (1,1) and ending point (N,W)
problem += x[0, 0] == 1  # Start at (1,1)
problem += x[N-1, W-1] == 1  # End at (N,W)

# Solve the problem
problem.solve()

# Output results
total_time = pulp.value(problem.objective)
paths = [(n + 1, w + 1) for n in range(N) for w in range(W) if pulp.value(x[n, w]) == 1]

output = {
    "paths": paths,
    "total_time": total_time
}

print(f' (Objective Value): <OBJ>{total_time}</OBJ>')
print(json.dumps(output))