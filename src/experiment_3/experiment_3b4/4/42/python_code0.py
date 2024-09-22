import pulp

# Data from the provided JSON
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [
        [0.0, 2.0, 5.0],
        [2.0, 0.0, 3.0],
        [5.0, 3.0, 0.0]
    ]
}

# Number of depots and ports
I = len(data['numdepot'])
J = len(data['numport'])

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['price'] * data['distance'][i][j] / 2 * x[i, j] for i in range(I) for j in range(J))

# Constraints
# Constraint: sum of x[i, j] over j should be less than or equal to numdepot[i] for all i
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= data['numdepot'][i]

# Constraint: sum of x[i, j] over i should be greater than or equal to numport[j] for all j
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= data['numport'][j]

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')