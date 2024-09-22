import pulp

# Data from the JSON format
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Number of depots and ports
I = len(data['numdepot'])
J = len(data['numport'])

# Create the problem
problem = pulp.LpProblem("Transportation_Cost_Minimization", pulp.LpMinimize)

# Decision variables
number = pulp.LpVariable.dicts("number", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((number[i][j] / 2) * data['distance'][i][j] * data['price'] for i in range(I) for j in range(J))

# Supply constraints
for i in range(I):
    problem += pulp.lpSum(number[i][j] for j in range(J)) <= data['numdepot'][i]

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(number[i][j] for i in range(I)) >= data['numport'][j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')