from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary, value

# Input data
data = {
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
}

N = data["N"]
distances = data["Distances"]
start_city = data["StartCity"]

# Define the problem
problem = LpProblem("Traveling_Salesman_Problem", LpMinimize)

# Variables
x = LpVariable.dicts("x", (range(N), range(N)), cat=LpBinary)
u = LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1, cat='Continuous')

# Objective Function
problem += lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N))

# Constraints
for i in range(N):
    problem += lpSum(x[i][j] for j in range(N) if j != i) == 1
    problem += lpSum(x[j][i] for j in range(N) if j != i) == 1

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N-1) * x[i][j] <= N-2

# Solve
problem.solve()

# Extract Results
visit_order = [start_city]
current_city = start_city

for _ in range(N):
    for next_city in range(N):
        if x[current_city][next_city].varValue == 1:
            visit_order.append(next_city)
            current_city = next_city
            break

# Calculate total distance
total_distance = value(problem.objective)

# Preparing output in required format
output = {
    "visit_order": visit_order + [start_city],
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')