import pulp
import json

# Input data
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')
west_time = data['west_time']
north_time = data['north_time']

N = len(north_time)
W = len(west_time[0])

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Transportation_Time", pulp.LpMinimize)

# Define decision variables
x_north = pulp.LpVariable.dicts("north", ((n, w) for n in range(N) for w in range(W)), cat='Binary')
x_west = pulp.LpVariable.dicts("west", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(north_time[n][w] * x_north[n, w] for n in range(N) for w in range(W)) +
    pulp.lpSum(west_time[n][w] * x_west[n, w] for n in range(N) for w in range(W))
)

# Constraints
for n in range(1, N-1):
    for w in range(1, W-1):
        problem += (x_north[n-1, w] + x_west[n, w-1] == x_north[n+1, w] + x_west[n, w+1])

problem += (x_north[0, 0] + x_west[0, 0] == 1)
problem += (x_west[N-1, W-1] + x_north[N-2, W-1] == 1)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')