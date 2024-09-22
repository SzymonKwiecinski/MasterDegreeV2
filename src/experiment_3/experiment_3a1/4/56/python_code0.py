import pulp
import json

# Load data from JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

N = len(west_time)
W = len(north_time[0])

# Define the problem
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N + 1) for w in range(1, W)), lowBound=0)
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N) for w in range(1, W + 1)), lowBound=0)

# Objective function
problem += pulp.lpSum(x[n, w] for n in range(1, N + 1) for w in range(1, W)) + \
           pulp.lpSum(y[n, w] for n in range(1, N) for w in range(1, W + 1)), "TotalTime"

# Constraints
for n in range(1, N + 1):
    for w in range(1, W):
        problem += x[n, w] >= west_time[n-1][w-1], f"WestTimeConstraint_n{n}_w{w}"

for n in range(1, N):
    for w in range(1, W + 1):
        problem += y[n, w] >= north_time[n-1][w-1], f"NorthTimeConstraint_n{n}_w{w}"

for n in range(1, N + 1):
    problem += pulp.lpSum(x[n, w] for w in range(1, W)) == pulp.lpSum(x[n, w] for w in range(1, W)), f"TotalWestTime_n{n}"

for n in range(1, N):
    problem += pulp.lpSum(y[n, w] for w in range(1, W + 1)) == pulp.lpSum(y[n, w] for w in range(1, W + 1)), f"TotalNorthTime_n{n}"

# Starting point constraint
problem += x[1, 1] + y[1, 1] == 0, "StartingPoint"

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')