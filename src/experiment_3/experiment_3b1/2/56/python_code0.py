import pulp
import json

# Given data in JSON format
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Extracting the dimensions
N = len(data['north_time'])    # Number of North steps
W = len(data['west_time'][0])  # Number of West steps

# Create the LP problem
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Creating decision variables
x = pulp.LpVariable.dicts("North", ((n, w) for n in range(N) for w in range(W)), 0, 1, pulp.LpBinary)
y = pulp.LpVariable.dicts("West", ((n, w) for n in range(N) for w in range(W-1)), 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum(data['west_time'][n][w] * y[n, w] + data['north_time'][n][w] * x[n, w] 
                       for n in range(N) for w in range(W-1)), "TotalTime"

# Constraints
# Flow conservation at each intersection
for n in range(N):
    problem += pulp.lpSum(y[n, w] for w in range(W-1)) == 1, f"FlowConservationNorth_{n}"

for w in range(W):
    problem += pulp.lpSum(x[n, w] for n in range(N)) == 1, f"FlowConservationWest_{w}"

# Movement restrictions
for n in range(N):
    for w in range(W-1):
        problem += x[n, w] + y[n, w] <= 1, f"MovementRestriction_{n}_{w}"

# Solve the problem
problem.solve()

# Output results
paths = []
for n in range(N):
    for w in range(W-1):
        if pulp.value(x[n, w]) == 1:
            paths.append(f"Move North from ({w}, {n}) to ({w}, {n + 1})")
        if pulp.value(y[n, w]) == 1:
            paths.append(f"Move West from ({w}, {n}) to ({w + 1}, {n})")

# Print the results
print("Optimal Paths:")
for path in paths:
    print(path)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')