import pulp
import json

# Data in JSON format
data_json = '''{
    "S": 3,
    "G": 2,
    "N": 4,
    "Capacity": [[15, 20], [20, 15], [5, 17]],
    "Population": [[7, 19], [4, 12], [9, 2], [6, 8]],
    "Distance": [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}'''

data = json.loads(data_json)

# Extracting parameters from data
S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create the problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distance[n][s] * x[n, s, g] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Capacity Constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_s{s}_g{g}"

# Demand Constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for s in range(S)) == population[n][g], f"Demand_Constraint_n{n}_g{g}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')