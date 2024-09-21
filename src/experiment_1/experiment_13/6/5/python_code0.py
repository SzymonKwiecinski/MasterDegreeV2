import pulp
import json

# Data provided in JSON format
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Extracting parameters from data
S = data['S']  # Number of schools
G = data['G']  # Number of student groups
N = data['N']  # Number of neighborhoods
Capacity = data['Capacity']  # School capacities for student groups
Population = data['Population']  # Student group populations in neighborhoods
Distance = data['Distance']  # Distances between neighborhoods and schools

# Create the problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(G), range(S)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(Distance[n][s] * x[n][g][s] for n in range(N) for g in range(G) for s in range(S)), "Total_Distance"

# Constraints
# 1. Total number of students assigned from neighborhood n to schools does not exceed the population of group g in neighborhood n
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for s in range(S)) <= Population[n][g], f"Population_Limit_n{n}_g{g}"

# 2. Total number of students assigned to school s does not exceed the capacity of school s for group g
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for n in range(N)) <= Capacity[s][g], f"Capacity_Limit_s{s}_g{g}"

# 3. Each student is assigned to exactly one school
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for s in range(S)) == Population[n][g], f"Exact_Assignment_n{n}_g{g}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')