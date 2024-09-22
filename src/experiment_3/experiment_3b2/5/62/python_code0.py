import pulp
import json

# Data
data_json = '''{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}'''
data = json.loads(data_json.replace("'", '"'))

N = data['N']
Distances = data['Distances']
C = list(range(N))

# Problem Definition
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (C, C), cat='Binary')
u = pulp.LpVariable.dicts("u", C, lowBound=0)

# Objective Function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in C for j in C if i != j), "Total Distance"

# Constraints
# Each city is departed exactly once
for i in C:
    problem += pulp.lpSum(x[i][j] for j in C if j != i) == 1, f"DepartOnce_{i}"

# Each city is arrived at exactly once
for j in C:
    problem += pulp.lpSum(x[i][j] for i in C if i != j) == 1, f"ArriveOnce_{j}"

# Subtour elimination
for i in C:
    for j in C:
        if i != j and i != 0 and j != 0:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"SubtourElim_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')