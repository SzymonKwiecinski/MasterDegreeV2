import pulp

# Data
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

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Sets
C = list(range(N))  # Cities set

# Problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in C for j in C if i != j), cat='Binary')
u = pulp.LpVariable.dicts("u", (i for i in C if i != start_city), lowBound=1, upBound=N, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in C for j in C if i != j)

# Constraints

# Flow constraints
for i in C:
    problem += pulp.lpSum(x[i, j] for j in C if i != j) == 1, f"OutFlow_{i}"
    problem += pulp.lpSum(x[j, i] for j in C if i != j) == 1, f"InFlow_{i}"

# Subtour elimination constraints using MTZ constraints
for i in C:
    for j in C:
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1, f"Subtour_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')