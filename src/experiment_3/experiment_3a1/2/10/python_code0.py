import pulp
import json

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
N = data['N']
S = data['S']
G = data['G']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Minimize_Student_Transportation_Distance", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(Distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Constraints

# Capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= Capacity[s][g], f"Capacity_Constraint_s{s}_g{g}"

# Demand constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == Population[n][g], f"Demand_Constraint_n{n}_g{g}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')