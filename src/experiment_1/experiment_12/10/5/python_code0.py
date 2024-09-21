import pulp

# Data
data = {
    'S': 3, 
    'G': 2, 
    'N': 4, 
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Parameters
S = data['S']
G = data['G']
N = data['N']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Problem
problem = pulp.LpProblem("School Assignment Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, g, s) for n in range(N) for g in range(G) for s in range(S)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(Distance[n][s] * x[n, g, s] for n in range(N) for g in range(G) for s in range(S)), "Total Distance"

# Constraints
# 1. Students from each group in each neighborhood do not exceed the population
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, g, s] for s in range(S)) <= Population[n][g], f"Population_Constraint_N{n}_G{g}"

# 2. Students from each group assigned to a school do not exceed the school's capacity for that group
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, g, s] for n in range(N)) <= Capacity[s][g], f"Capacity_Constraint_S{s}_G{g}"

# 3. Each student is assigned to exactly one school
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, g, s] for s in range(S)) == Population[n][g], f"Assignment_Constraint_N{n}_G{g}"

# Solve the Problem
problem.solve()

# Output the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')