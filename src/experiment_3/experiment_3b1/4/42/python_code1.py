import pulp
import json

# Data from the provided JSON format
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Indices
I = len(data['numdepot'])  # Number of depots
J = len(data['numport'])    # Number of ports

# Create the Linear Programming problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision Variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((number[i, j] / 2.0) * data['price'] * data['distance'][i][j] for i in range(I) for j in range(J))

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= data['numdepot'][i]

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= data['numport'][j]

# Solve the problem
problem.solve()

# Output the number of containers sent from each depot to each port
output = [[pulp.value(number[i, j]) for j in range(J)] for i in range(I)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps({"number": output}))