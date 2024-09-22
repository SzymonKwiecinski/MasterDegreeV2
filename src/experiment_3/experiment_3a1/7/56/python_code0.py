import pulp
import json

# Data provided in JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')

# Extracting the west_time and north_time matrices
west_time = data['west_time']
north_time = data['north_time']

N = len(west_time)  # Number of north intersections
W = len(north_time[0]) + 1  # Number of west intersections (W = columns of north_time + 1)

# Initialize the problem
problem = pulp.LpProblem("OptimalDeliveryPath", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N + 1) for w in range(1, W + 1)), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(west_time[n - 1][w - 1] * x[n, w] for n in range(1, N + 1) for w in range(1, W)) +
    pulp.lpSum(north_time[n - 1][w - 1] * x[n, w] for n in range(1, N) for w in range(1, W + 1))
), "TotalTravelTime"

# Constraints
# Flow Conservation
for n in range(1, N + 1):
    for w in range(1, W):
        problem += (
            pulp.lpSum(x[n, w] for w in range(1, W)) + 
            pulp.lpSum(x[n, w] for n in range(1, N)) == 1,
            f"FlowConservation_{n}_{w}"
        )

# Start and End Points
problem += (pulp.lpSum(x[1, 1]) == 1, "StartPoint")
problem += (pulp.lpSum(x[N, W]) == 1, "EndPoint")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')