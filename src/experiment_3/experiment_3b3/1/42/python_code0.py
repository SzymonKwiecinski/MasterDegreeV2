import pulp

# Data from JSON
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Indices for depots and ports
I = range(len(data['numdepot']))  # Depots
J = range(len(data['numport']))   # Ports

# Problem definition
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in I for j in J), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((x[i, j] / 2) * data['distance'][i][j] * data['price'] for i in I for j in J)

# Supply constraints at each depot
for i in I:
    problem += pulp.lpSum(x[i, j] for j in J) <= data['numdepot'][i]

# Demand constraints at each port
for j in J:
    problem += pulp.lpSum(x[i, j] for i in I) >= data['numport'][j]

# Solve the problem
problem.solve()

# Output the number of containers sent from each depot to each port
output = {'number': [[x[i, j].varValue for j in J] for i in I]}

print("Output:", output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')