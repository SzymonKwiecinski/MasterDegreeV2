import pulp

# Data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Indices
I = len(data['numdepot'])
J = len(data['numport'])

# Create the LP problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((number[i, j] / 2) * data['price'] * data['distance'][i][j] for i in range(I) for j in range(J))

# Constraints
# Supply constraints
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= data['numdepot'][i]

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= data['numport'][j]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')