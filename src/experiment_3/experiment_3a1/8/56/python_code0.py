import pulp
import json

# Data
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

# Parameters
N = len(north_time) + 1  # Total number of streets (vertical)
W = len(west_time[0]) + 1  # Total number of avenues (horizontal)

# Define the problem
problem = pulp.LpProblem("DeliveryPathOptimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(1, N), range(1, W)), cat='Binary')
y = pulp.LpVariable.dicts("y", (range(1, N), range(1, W)), cat='Binary')

# Objective Function
problem += pulp.lpSum(west_time[n-1][w-1] * x[n][w] + north_time[n-1][w-1] * y[n][w] 
                       for n in range(1, N) for w in range(1, W)), "TotalWalkingTime"

# Constraints
for n in range(1, N):
    problem += pulp.lpSum(x[n][w] for w in range(1, W)) + pulp.lpSum(y[n][w] for w in range(1, W)) == 1, f"FlowConservation_n_{n}"

for w in range(1, W):
    problem += pulp.lpSum(x[n][w] for n in range(1, N)) + pulp.lpSum(y[n][w] for n in range(1, N)) == 1, f"FlowConservation_w_{w}"

# Solve the problem
problem.solve()

# Output results
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[n][w]) == 1 or pulp.value(y[n][w]) == 1]
total_time = pulp.value(problem.objective)

# Print the desired outputs
print(f'Paths: {paths}')
print(f'Total time: {total_time}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')