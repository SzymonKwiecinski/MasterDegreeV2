import pulp

# Define the LP problem
problem = pulp.LpProblem("Shortest_Path_Problem", pulp.LpMinimize)

# Parse the data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Get grid dimensions
N = len(data['north_time']) + 1
W = len(data['west_time'][0]) + 1

# Define decision variables for paths (binary variables)
paths = pulp.LpVariable.dicts("Path", ((n, w, direction) for n in range(N) for w in range(W) for direction in ['W', 'N']),
                              cat='Binary')

# Define objective function
problem += pulp.lpSum([paths[n, w, 'W'] * data['west_time'][n][w] for n in range(N) for w in range(W-1)]) + \
           pulp.lpSum([paths[n, w, 'N'] * data['north_time'][n][w] for n in range(N-1) for w in range(W)])

# Add constraints
for n in range(N):
    for w in range(W):
        if n < N - 1 and w < W - 1:
            problem += paths[n, w, 'W'] + paths[n, w, 'N'] <= 1

# Flow constraints
problem += pulp.lpSum([paths[0, 0, 'N'], paths[0, 0, 'W']]) == 1

for n in range(1, N):
    problem += pulp.lpSum([paths[n-1, w, 'N'] for w in range(W)]) == \
               pulp.lpSum([paths[n, w, 'N'] for w in range(W)])

for w in range(1, W):
    problem += pulp.lpSum([paths[n, w-1, 'W'] for n in range(N)]) == \
               pulp.lpSum([paths[n, w, 'W'] for n in range(N)])

# Solve the problem
problem.solve()

# Extract solution
solution_paths = [(n, w) for n in range(N) for w in range(W) if pulp.value(paths[n, w, 'W']) == 1 or pulp.value(paths[n, w, 'N']) == 1]
total_travel_time = pulp.value(problem.objective)

# Formulate output
output = {
    "paths": solution_paths,
    "total_time": total_travel_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')