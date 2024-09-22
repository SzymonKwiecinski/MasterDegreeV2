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
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", 
                            ((n, s, g) for n in range(data['N']) 
                                        for s in range(data['S']) 
                                        for g in range(data['G'])), 
                            lowBound=0)

# Objective function: minimize total distance
problem += pulp.lpSum(data['Distance'][n][s] * x[n, s, g] 
                       for n in range(data['N']) 
                       for s in range(data['S']) 
                       for g in range(data['G'])), "Total_Distance"

# Constraints: Population must be assigned
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, s, g] for s in range(data['S'])) == data['Population'][n][g]

# Constraints: School capacity
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, s, g] for n in range(data['N'])) <= data['Capacity'][s][g]

# Solve the problem
problem.solve()

# Prepare the output
assignment = [[[x[n, s, g].varValue for g in range(data['G'])] 
                for s in range(data['S'])] 
                for n in range(data['N'])]

total_distance = pulp.value(problem.objective)

# Output the result
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')

# If needed to return output
output