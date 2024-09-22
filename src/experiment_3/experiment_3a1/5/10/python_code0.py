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

# Problem setup
problem = pulp.LpProblem("Student_Assignment_to_Schools", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", 
                           ((n, s, g) for n in range(data['N']) for s in range(data['S']) for g in range(data['G'])), 
                           lowBound=0, 
                           cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Distance'][n][s] * x[n, s, g] for n in range(data['N']) 
                      for s in range(data['S']) 
                      for g in range(data['G'])), "Total_Distance"

# Capacity constraints
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, s, g] for n in range(data['N'])) <= data['Capacity'][s][g], f"Capacity_Constraint_S{s}_G{g}"

# Population constraints
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, s, g] for s in range(data['S'])) == data['Population'][n][g], f"Population_Constraint_N{n}_G{g}"

# Solve the problem
problem.solve()

# Output results
assignment = {(n, s, g): x[n, s, g].varValue for n in range(data['N']) for s in range(data['S']) for g in range(data['G'])}
total_distance = pulp.value(problem.objective)

print("Student Assignment (x):")
for key, value in assignment.items():
    print(f"x[{key[0]},{key[1]},{key[2]}] = {value}")

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')