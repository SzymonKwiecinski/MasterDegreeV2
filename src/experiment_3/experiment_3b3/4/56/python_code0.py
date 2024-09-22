import pulp

# Data
data = {
    'west_time': [[3.5, 4.5], [4, 4], [5, 4]],
    'north_time': [[10, 10, 9], [9, 9, 12]]
}

west_time = data['west_time']
north_time = data['north_time']

N = len(north_time) + 1  # Total streets (north direction)
W = len(west_time[0]) + 1  # Total avenues (west direction)

# Problem
problem = pulp.LpProblem("Minimize_Travel_Time", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((w, n) for n in range(1, N) for w in range(1, W)), cat='Binary')
y = pulp.LpVariable.dicts("y", ((w, n) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective
problem += pulp.lpSum(west_time[n-1][w-1] * x[(w, n)] + north_time[n-1][w-1] * y[(w, n)]
                      for n in range(1, N) for w in range(1, W))

# Constraints
for n in range(1, N):
    for w in range(1, W):
        problem += x[(w, n)] + y[(w, n)] == 1, f"Outgoing_Path_{w}_{n}"

# Solve
problem.solve()

# Output
for n in range(1, N):
    for w in range(1, W):
        if x[(w, n)].varValue > 0.5:
            print(f"Path goes west from ({w}, {n})")
        if y[(w, n)].varValue > 0.5:
            print(f"Path goes north from ({w}, {n})")

print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")