import pulp
import json

# Input data
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Problem definition
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(data['N']), range(data['G']), range(data['S'])), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Distance'][n][s] * x[n][g][s] for n in range(data['N']) for g in range(data['G']) for s in range(data['S'])), "Total_Distance"

# Constraints

# 1. Total number of students assigned from each group in each neighborhood does not exceed the population
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][g][s] for s in range(data['S'])) <= data['Population'][n][g], f"Population_Constraint_n{n}_g{g}"

# 2. Total assigned to each school does not exceed its capacity for that group
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][g][s] for n in range(data['N'])) <= data['Capacity'][s][g], f"Capacity_Constraint_s{s}_g{g}"

# 3. Each student in each neighborhood is assigned to exactly one school
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][g][s] for s in range(data['S'])) == data['Population'][n][g], f"Assignment_Constraint_n{n}_g{g}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')