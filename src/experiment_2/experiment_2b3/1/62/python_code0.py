import pulp
import json

# Data
data_json = '''<DATA>
{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}
</DATA>'''
data = json.loads(data_json)

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N) if i != j), cat='Binary')
u = pulp.LpVariable.dicts('u', range(N), lowBound=0, upBound=N-1, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if i != j) == 1
    problem += pulp.lpSum(x[j, i] for j in range(N) if i != j) == 1

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i, j] <= N - 2
            
# Solve the problem
problem.solve()

# Retrieve the solution
visit_order = [start_city]
current_city = start_city
while len(visit_order) < N + 1:
    for j in range(N):
        if current_city != j and pulp.value(x[current_city, j]) == 1:
            visit_order.append(j)
            current_city = j
            break

total_distance = pulp.value(problem.objective)

# Output
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')