import pulp
import json

# Data provided in JSON format
data = {'S': 3, 'G': 2, 'N': 4, 
        'Capacity': [[15, 20], [20, 15], [5, 17]], 
        'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
        'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

# Parameters
S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create the problem variable
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G))

# Capacity Constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_s{S}_g{G}"

# Demand Constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Demand_Constraint_n{N}_g{G}"

# Solve the problem
problem.solve()

# Output the decision variables and the total distance
assignment = [[[[x[n][s][g].varValue for g in range(G)] for s in range(S)] for n in range(N)]]
total_distance = pulp.value(problem.objective)

# Printing the results
print("Assignment (x[n][s][g]):", assignment)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')