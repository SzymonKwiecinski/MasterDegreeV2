import pulp
import json

data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Create the problem variable
problem = pulp.LpProblem("Transport_Problem", pulp.LpMinimize)

# Decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function: minimize total transportation cost
problem += pulp.lpSum(number[i, j] * distance[i][j] * price / 2 for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= numdepot[i], f"Depot_Supply_Constraint_{i}"

# Demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= numport[j], f"Port_Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "number": [[number[i, j].varValue for j in range(J)] for i in range(I)]
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')