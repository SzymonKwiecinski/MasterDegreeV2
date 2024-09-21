import pulp
import json

# Data from the provided JSON format
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Define the problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, g, s) for n in range(data['N']) for g in range(data['G']) for s in range(data['S'])), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Distance'][n][s] * x[n, g, s] for n in range(data['N']) for g in range(data['G']) for s in range(data['S'])), "Total_Distance"

# Constraints
# Constraint 1: Population limit in each neighborhood
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, g, s] for s in range(data['S'])) <= data['Population'][n][g], f"Population_Constraint_n{n}_g{g}"

# Constraint 2: School capacity limit
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, g, s] for n in range(data['N'])) <= data['Capacity'][s][g], f"Capacity_Constraint_s{s}_g{g}"

# Constraint 3: Every student is assigned to exactly one school
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, g, s] for s in range(data['S'])) == data['Population'][n][g], f"One_School_Assignment_n{n}_g{g}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')