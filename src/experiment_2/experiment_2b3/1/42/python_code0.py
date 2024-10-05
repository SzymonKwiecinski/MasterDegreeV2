import pulp

# Problem data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Number of depots and ports
I = len(data['numdepot'])
J = len(data['numport'])

# Create the LP problem
problem = pulp.LpProblem("Transport_Containers", pulp.LpMinimize)

# Decision variables
x = [[pulp.LpVariable(f'x_{i}_{j}', lowBound=0, cat='Continuous') for j in range(J)] for i in range(I)]

# Objective function
objective = pulp.lpSum(data['price'] * data['distance'][i][j] * (x[i][j] / 2) for i in range(I) for j in range(J))
problem += objective

# Constraints
# Each depot can supply containers up to its limit
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= data['numdepot'][i]

# Each port requires a certain number of containers
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) == data['numport'][j]

# Solve the problem
problem.solve()

# Extract the solution
number = [[x[i][j].varValue for j in range(J)] for i in range(I)]

# Output the solution
solution = {"number": number}

# Print the solution
print(solution)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')