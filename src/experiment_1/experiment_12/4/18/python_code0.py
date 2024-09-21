import pulp

# Load the data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

# Parameters
N = data['N']
Distances = data['Distances']
StartCity = data['StartCity']

# Problem
problem = pulp.LpProblem('TravelingSalesmanProblem', pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', [(i, j) for i in range(N) for j in range(N)], cat='Binary')
u = pulp.LpVariable.dicts('u', [i for i in range(N)], lowBound=1, upBound=N-1, cat='Continuous')

# Objective Function
problem += pulp.lpSum(Distances[i][j] * x[i, j] for i in range(N) for j in range(N)), "TotalTravelDistance"

# Constraints
# 1. Each town must be visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1, f"VisitExact_{i}"
    problem += pulp.lpSum(x[j, i] for j in range(N) if j != i) == 1, f"BeVisitedExact_{i}"

# 2. The traveler must return to the StartCity after visiting all other towns
problem += pulp.lpSum(x[StartCity, j] for j in range(N) if j != StartCity) == 1, "StartCityOut"
problem += pulp.lpSum(x[i, StartCity] for i in range(N) if i != StartCity) == 1, "StartCityIn"

# 3. Eliminate subtours (Miller-Tucker-Zemlin formulation)
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1, f"SubtourElimination_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')