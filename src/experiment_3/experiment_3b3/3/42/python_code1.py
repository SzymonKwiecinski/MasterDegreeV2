import pulp

# Data from JSON
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

# Problem definition
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Number of depots and ports
I = len(data['numdepot'])
J = len(data['numport'])

# Decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((number[i, j] * data['distance'][i][j] * data['price']) / 2 for i in range(I) for j in range(J))

# Supply constraints for each depot
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= data['numdepot'][i], f"Supply_Constraint_{i}"

# Demand constraints for each port
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= data['numport'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')