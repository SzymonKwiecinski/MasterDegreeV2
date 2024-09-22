import pulp

# Load data
data = {
    'N': 6,
    'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], 
                  [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], 
                  [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]],
    'StartCity': 0
}

N = data['N']
Distances = data['Distances']
StartCity = data['StartCity']

# Create a LP problem
problem = pulp.LpProblem('Traveling_Salesman_Problem', pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat=pulp.LpBinary)
u = pulp.LpVariable.dicts('u', (i for i in range(1, N)), lowBound=1, upBound=N-1, cat=pulp.LpInteger)

# Objective Function
problem += pulp.lpSum(Distances[i][j] * x[i, j] for i in range(N) for j in range(N)), 'Minimize_Total_Distance'

# Constraints
# Each city is visited exactly once
for i in range(N):
    if i != StartCity:
        problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1
        problem += pulp.lpSum(x[j, i] for j in range(N) if j != i) == 1

# Start city constraints (start and return)
problem += pulp.lpSum(x[StartCity, j] for j in range(N) if j != StartCity) == 1
problem += pulp.lpSum(x[j, StartCity] for j in range(N) if j != StartCity) == 1

# Subtour elimination
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')