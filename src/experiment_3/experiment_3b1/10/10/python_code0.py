import pulp

# Data provided in the JSON format
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

# Decision Variables
x = pulp.LpVariable.dicts("x", 
                           ((n, s, g) 
                            for n in range(data['N']) 
                            for s in range(data['S']) 
                            for g in range(data['G'])), 
                           lowBound=0, 
                           cat='Integer')

# Objective Function: Minimize total distance
problem += pulp.lpSum(data['Distance'][n][s] * x[n, s, g] 
                       for n in range(data['N']) 
                       for s in range(data['S']) 
                       for g in range(data['G'])), "Total_Distance"

# Capacity Constraints
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, s, g] for n in range(data['N'])) <= data['Capacity'][s][g], f"Capacity_S{S}_G{G}"

# Demand Constraints
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, s, g] for s in range(data['S'])) == data['Population'][n][g], f"Demand_N{n}_G{g}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')