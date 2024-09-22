import pulp
import json

# Provided data in JSON format
data = '''
{
    "S": 3,
    "G": 2,
    "N": 4,
    "Capacity": [[15, 20], [20, 15], [5, 17]],
    "Population": [[7, 19], [4, 12], [9, 2], [6, 8]],
    "Distance": [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}
'''
data = json.loads(data)

# Problem initialization
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", (range(data['N']), range(data['S']), range(data['G'])), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Distance'][n][s] * x[n][s][g] for n in range(data['N']) for s in range(data['S']) for g in range(data['G'])), "Total_Distance"

# Capacity Constraints
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][s][g] for n in range(data['N'])) <= data['Capacity'][s][g], f"Capacity_{s}_{g}"

# Population Constraints
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][s][g] for s in range(data['S'])) == data['Population'][n][g], f"Population_{n}_{g}"

# Solve the problem
problem.solve()

# Output results
for n in range(data['N']):
    for s in range(data['S']):
        for g in range(data['G']):
            print(f"x[{n},{s},{g}] = {x[n][s][g].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')