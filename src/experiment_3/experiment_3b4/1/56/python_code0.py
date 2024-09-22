import pulp

# Data provided
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

# Dimensions
N = len(north_time) + 1  # Number of streets
W = len(west_time[0]) + 1  # Number of avenues

# Problem Definition
problem = pulp.LpProblem("Optimal_Path_Travel_Time_Minimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N+1) for w in range(1, W)), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, w) for n in range(1, N) for w in range(1, W+1)), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * x[n, w] for n in range(1, N) for w in range(1, W-1)) +
    pulp.lpSum(north_time[n-1][w-1] * y[n, w] for n in range(1, N) for w in range(1, W))
)

# Constraints

# Flow Conservation
for n in range(1, N):
    for w in range(1, W):
        problem += (x.get((n, w), 0) + y[n, w] == 1)

# North Movement Constraints
for w in range(1, W):
    problem += (pulp.lpSum(y[n, w] for n in range(1, N)) == N - 1)

# West Movement Constraints
for n in range(1, N):
    problem += (pulp.lpSum(x[n, w] for w in range(1, W - 1)) == W - 1)

# Initial and Terminal Conditions
problem += x[1, 1] == 0
problem += y[1, 1] == 0
problem += x[N-1, W-1] == 1
problem += y[N-1, W] == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')