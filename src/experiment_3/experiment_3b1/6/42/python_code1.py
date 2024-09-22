import pulp
import json

# Input data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Number of depots and ports
I = len(data['numdepot'])
J = len(data['numport'])

# Creating the LP problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision variables
number = pulp.LpVariable.dicts("number", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((number[i][j] * data['price'] * data['distance'][i][j]) / 2 for i in range(I) for j in range(J))

# Supply constraints
for i in range(I):
    problem += pulp.lpSum(number[i][j] for j in range(J)) <= data['numdepot'][i]

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(number[i][j] for i in range(I)) >= data['numport'][j]

# Solve the problem
problem.solve()

# Prepare output
output = [[number[i][j].varValue for i in range(I)] for j in range(J)]

# Print objective value and output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'{"number": {output}}')