import pulp

# Parse the data
data = {
    'N': 6, 
    'Distances': [
        [0, 182, 70, 399, 56, 214], 
        [182, 0, 255, 229, 132, 267], 
        [70, 255, 0, 472, 127, 287], 
        [399, 229, 472, 0, 356, 484], 
        [56, 132, 127, 356, 0, 179], 
        [214, 267, 287, 484, 179, 0]
    ], 
    'StartCity': 0
}

# Create the problem
problem = pulp.LpProblem("TravelingSalesman", pulp.LpMinimize)

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Decision Variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', (i for i in range(N)), lowBound=0, upBound=N-1, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N)), "Total Distance"

# Constraints
# Each town must be visited exactly once
for j in range(N):
    problem += pulp.lpSum(x[start_city, j] for j in range(N)) == 1

# From each town, leave to another town
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) == 1
    
# Returning to the start city
problem += pulp.lpSum(x[i, start_city] for i in range(N)) == 1

# Subtour elimination
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Solve the problem
problem.solve()

# Print Objective
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')