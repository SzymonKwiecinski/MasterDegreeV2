import pulp

# Data from JSON
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

# Dimensions
N = len(data['north_time']) + 1  # Assuming north_time represents rows minus 1
W = len(data['west_time'][0]) + 1  # Assuming west_time represents columns minus 1

# Define the Linear Programming problem
problem = pulp.LpProblem("Delivery_Path_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective function
problem += pulp.lpSum(data['west_time'][n-1][w-1] * x[(n, w)] +
                      data['north_time'][n-1][w-1] * x[(n, w)]
                      for n in range(1, N) for w in range(1, W))

# Constraints

# Flow Conservation Constraints
problem += pulp.lpSum(x[(1, w)] for w in range(1, W)) == 1  # Start at (1,1)
problem += pulp.lpSum(x[(n, W-1)] for n in range(1, N)) == 1  # End at (W,N)

# Movement Constraints
for n in range(1, N-1):
    for w in range(1, W-1):
        problem += x[(n, w)] == x[(n, w+1)] + x[(n+1, w)]

# Binary Constraints are inherent in the variable definition

# Solve the problem
problem.solve()

# Output the results
paths = [(n, w) for n in range(1, N) for w in range(1, W) if pulp.value(x[(n, w)]) == 1]
total_time = pulp.value(problem.objective)

print(f'Paths (Intersections): {paths}')
print(f'Total Time (Objective Value): <OBJ>{total_time}</OBJ>')