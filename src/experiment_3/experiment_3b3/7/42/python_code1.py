import pulp

# Data from JSON
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Number of depots and ports
I = len(data['numdepot'])
J = len(data['numport'])

# Problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision Variables
number_vars = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((number_vars[i, j] * data['price'] * data['distance'][i][j]) / 2 for i in range(I) for j in range(J))

# Constraints
# Depot capacity constraints
for i in range(I):
    problem += pulp.lpSum(number_vars[i, j] for j in range(J)) <= data['numdepot'][i]

# Port demand constraints
for j in range(J):
    problem += pulp.lpSum(number_vars[i, j] for i in range(I)) == data['numport'][j]

# Solve the problem
problem.solve()

# Print the results
for i in range(I):
    for j in range(J):
        print(f'number[{i},{j}] = {number_vars[i, j].varValue}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')