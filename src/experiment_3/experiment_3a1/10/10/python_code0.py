import pulp
import json

# Given data in JSON format
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

# Define sets
S = range(data['S'])  # Schools
G = range(data['G'])  # Grades
N = range(data['N'])  # Neighborhoods

# Decision Variables
x = pulp.LpVariable.dicts("x", (N, S, G), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Distance'][n][s] * x[n][s][g] for n in N for s in S for g in G), "Total_Distance"

# Capacity Constraints
for s in S:
    for g in G:
        problem += pulp.lpSum(x[n][s][g] for n in N) <= data['Capacity'][s][g], f"Capacity_Constraint_{s}_{g}"

# Demand Constraints
for n in N:
    for g in G:
        problem += pulp.lpSum(x[n][s][g] for s in S) == data['Population'][n][g], f"Demand_Constraint_{n}_{g}"

# Solve the problem
problem.solve()

# Print the results
for n in N:
    for s in S:
        for g in G:
            print(f"Students from Neighborhood {n} Grade {g} assigned to School {s}: {x[n][s][g].varValue}")

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')