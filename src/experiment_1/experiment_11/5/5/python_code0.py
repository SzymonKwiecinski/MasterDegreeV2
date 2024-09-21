import pulp
import json

# Data from JSON format
data = {'S': 3, 'G': 2, 'N': 4, 
        'Capacity': [[15, 20], [20, 15], [5, 17]], 
        'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
        'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], 
                     [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

# Parameters
S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Decision Variables
x = pulp.LpVariable.dicts('x', (range(N), range(G), range(S)), lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(distance[n][s] * x[n][g][s] for n in range(N) for g in range(G) for s in range(S)), "Total_Distance"

# Constraints
# 1. Total number of students from each student group g assigned from neighborhood n does not exceed population
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for s in range(S)) <= population[n][g], f"Population_Constraint_{n}_{g}"

# 2. Total number of students from each student group g assigned to school s does not exceed capacity
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_{s}_{g}"

# 3. Each student is assigned to exactly one school
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for s in range(S)) == population[n][g], f"Assignment_Constraint_{n}_{g}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')