import pulp
import json

# Input data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Parameters
I = len(data['numdepot'])  # Number of depots
J = len(data['numport'])    # Number of ports
numdepot = data['numdepot']  # Number of containers at each depot
numport = data['numport']    # Number of containers required at each port
price = data['price']        # Transportation cost per km
distance = data['distance']  # Distance matrix

# Define the problem
problem = pulp.LpProblem("Container_Transport_Problem", pulp.LpMinimize)

# Decision Variables
number = pulp.LpVariable.dicts("number", [(i, j) for i in range(I) for j in range(J)], lowBound=0)

# Objective Function
problem += pulp.lpSum(0.5 * number[i, j] * distance[i][j] * price for i in range(I) for j in range(J))

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= numdepot[i]

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= numport[j]

# Solve the problem
problem.solve()

# Output results
output = {
    "number": [[pulp.value(number[i, j]) for j in range(J)] for i in range(I)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')