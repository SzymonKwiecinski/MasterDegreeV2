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

S = data['S']
G = data['G']
N = data['N']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Problem
problem = pulp.LpProblem("Student_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), 
                          lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(Distance[n][s] * x[(n, s, g)] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Constraints

# Capacity Constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[(n, s, g)] for n in range(N)) <= Capacity[s][g], f"Capacity_S{s}_G{g}"

# Population Constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[(n, s, g)] for s in range(S)) == Population[n][g], f"Population_N{n}_G{g}"

# Solve
problem.solve()

# Objective Value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")