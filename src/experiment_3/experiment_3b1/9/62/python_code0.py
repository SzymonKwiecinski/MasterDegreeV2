import pulp
import json

# Given data
data_json = '''{
    "N": 6,
    "Distances": [
        [0, 182, 70, 399, 56, 214], 
        [182, 0, 255, 229, 132, 267], 
        [70, 255, 0, 472, 127, 287], 
        [399, 229, 472, 0, 356, 484], 
        [56, 132, 127, 356, 0, 179], 
        [214, 267, 287, 484, 179, 0]
    ],
    "StartCity": 0
}'''

data = json.loads(data_json)
N = data['N']
distance = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1)

# Objective Function
problem += pulp.lpSum(distance[i][j] * x[i][j] for i in range(N) for j in range(N))

# Constraints
# Each town other than the start city must be visited exactly once
problem += pulp.lpSum(x[start_city][j] for j in range(N) if j != start_city) == 1
problem += pulp.lpSum(x[i][start_city] for i in range(N) if i != start_city) == 1

# Each town must be entered and exited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) == 1
    problem += pulp.lpSum(x[j][i] for j in range(N)) == 1

# Subtour elimination constraints
for i in range(N):
    for j in range(N):
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Output the results
visit_order = []
for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1 and i == start_city:
            visit_order.append(j)

total_distance = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')