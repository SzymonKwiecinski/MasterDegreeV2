import pulp
import json

# Data input
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 
        'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Define the problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
I = len(numdepot)
J = len(numport)

# Create a variable for each depot-port pair
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), 
                             lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(price * distance[i][j] * (x[i, j] / 2) for i in range(I) for j in range(J))

# Constraints
# Depot constraints: sum of containers sent from each depot should not exceed available containers
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i]

# Port constraints: sum of containers received at each port should meet the requirements
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j]

# Solve the problem
problem.solve()

# Create output
output = {
    "number": [[x[i, j].varValue for j in range(J)] for i in range(I)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print output
print(json.dumps(output))