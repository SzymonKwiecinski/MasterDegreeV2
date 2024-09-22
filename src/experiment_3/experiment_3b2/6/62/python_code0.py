import pulp
import json

# Data from the provided JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], 
                               [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], 
                               [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create a linear programming problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0)

# Objective function: Minimize total traveled distance
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
# Leave each city (for all cities except the start city)
for i in range(N):
    if i != start_city:
        problem += pulp.lpSum(x[i, j] for j in range(N)) == 1

# Enter each city (for all cities except the start city)
for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[i, j] for i in range(N)) == 1

# Leave start city
problem += pulp.lpSum(x[start_city, j] for j in range(N)) == 1

# Enter start city
problem += pulp.lpSum(x[i, start_city] for i in range(N)) == 1

# MTZ subtour elimination constraints
for i in range(N):
    for j in range(N):
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Start city's position in tour
problem += u[start_city] == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')