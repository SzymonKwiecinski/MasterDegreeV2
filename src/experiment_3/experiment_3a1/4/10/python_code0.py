import pulp
import json

# Input data in JSON format
data_json = '''
{
    "S": 3,
    "G": 2,
    "N": 4,
    "Capacity": [
        [15, 20],
        [20, 15],
        [5, 17]
    ],
    "Population": [
        [7, 19],
        [4, 12],
        [9, 2],
        [6, 8]
    ],
    "Distance": [
        [5.2, 4.0, 3.1],
        [3.8, 5.5, 6.1],
        [4.2, 3.5, 5.0],
        [5.0, 4.1, 3.2]
    ]
}
'''

# Load data
data = json.loads(data_json)

# Parameters
N = data['N']  # Number of neighborhoods
S = data['S']  # Number of schools
G = data['G']  # Number of grades
capacity = data['Capacity']  # Capacity of schools
population = data['Population']  # Population of students in neighborhoods
distance = data['Distance']  # Distance from neighborhoods to schools

# Define the problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_s{s}_g{g}"

# Demand constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Demand_Constraint_n{n}_g{g}"

# Solve the problem
problem.solve()

# Print the results
assignment = {f"x[{n}][{s}][{g}]": x[n][s][g].varValue for n in range(N) for s in range(S) for g in range(G)}
total_distance = pulp.value(problem.objective)

print("Assignment Structure:")
for key, value in assignment.items():
    print(f"{key}: {value}")

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')