import pulp

# Data
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

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(I) for j in range(J)], lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((x[i, j] * distance[i][j] * price / 2) for i in range(I) for j in range(J))

# Constraints
# Supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i]

# Demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j]

# Solve the problem
problem.solve()

# Output Results
output = {'number': [[pulp.value(x[i, j]) for i in range(I)] for j in range(J)]}
print(output)

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')