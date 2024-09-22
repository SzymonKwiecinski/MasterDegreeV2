import pulp
import json

data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[i, j] * distance[i][j] * price / 2 for i in range(I) for j in range(J)), "Total_Cost"

# Constraints for depots
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i], f"Depot_Constraint_{i}"

# Constraints for ports
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j], f"Port_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
number = [[x[i, j].varValue for j in range(J)] for i in range(I)]
output = {"number": number}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')