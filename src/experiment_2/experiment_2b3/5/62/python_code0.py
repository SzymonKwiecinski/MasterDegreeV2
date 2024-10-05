import pulp
import itertools

# Data from the input
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
Distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', range(N), lowBound=0, upBound=N-1, cat='Continuous')

# Objective function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in range(N) for j in range(N))

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1
    
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N-1

# Solve the problem
problem.solve()

# Retrieve the visit order
visit_order = [start_city]
current_city = start_city

for step in range(N):
    next_city = [j for j in range(N) if pulp.value(x[current_city][j]) == 1][0]
    visit_order.append(next_city)
    current_city = next_city

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Output format
output = {
    "visit_order": visit_order + [start_city],
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')