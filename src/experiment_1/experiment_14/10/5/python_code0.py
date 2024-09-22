import pulp

# Data extracted from JSON
S = 3  # Total number of schools
G = 2  # Total number of student groups
N = 4  # Total number of neighborhoods

# Capacity of each school for each student group
Capacity = [
    [15, 20],
    [20, 15],
    [5, 17]
]

# Population of each student group in each neighborhood
Population = [
    [7, 19],
    [4, 12],
    [9, 2],
    [6, 8]
]

# Distance from each neighborhood to each school
Distance = [
    [5.2, 4.0, 3.1],
    [3.8, 5.5, 6.1],
    [4.2, 3.5, 5.0],
    [5.0, 4.1, 3.2]
]

# Initialize the problem
problem = pulp.LpProblem("SchoolAssignmentProblem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, g, s) for n in range(N) for g in range(G) for s in range(S)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(Distance[n][s] * x[n, g, s] for n in range(N) for g in range(G) for s in range(S))

# Constraint 1: Students from each group in each neighborhood to schools does not exceed the population
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, g, s] for s in range(S)) == Population[n][g]

# Constraint 2: Students from each group to each school does not exceed the school's capacity
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, g, s] for n in range(N)) <= Capacity[s][g]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')