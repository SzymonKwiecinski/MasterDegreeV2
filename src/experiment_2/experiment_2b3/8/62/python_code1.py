import pulp
from itertools import combinations

# Define the data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

# Extract details from data
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N) if i != j), cat='Binary')
u = pulp.LpVariable.dicts("u", (i for i in range(1, N)), lowBound=0, upBound=N-1, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    if i != start_city:
        problem += pulp.lpSum(x[i, j] for j in range(N) if i != j) == 1
        problem += pulp.lpSum(x[j, i] for j in range(N) if i != j) == 1

# Subtour elimination constraints
for (i, j) in combinations(range(1, N), 2):
    problem += u[i] - u[j] + N * x[i, j] <= N - 1
    problem += u[j] - u[i] + N * x[j, i] <= N - 1

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=False, maxSeconds=10))

# Check if the problem has an optimal solution
if problem.status == pulp.LpStatusOptimal:
    # Extract the solution
    route = [start_city]
    current_city = start_city
    visit_set = set(range(N))
    while len(route) < N:
        for j in visit_set - set(route):
            if pulp.value(x[current_city, j]) == 1:
                route.append(j)
                current_city = j
                break
    route.append(start_city)

    # Calculate the total distance
    total_distance = sum(distances[route[i]][route[i+1]] for i in range(len(route)-1))

    # Print results
    output = {
        "visit_order": route,
        "total_distance": total_distance
    }
    import json
    print(json.dumps(output, indent=2))

    print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
else:
    print("No optimal solution found.")