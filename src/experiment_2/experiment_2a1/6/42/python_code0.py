import pulp
import json

data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
number = pulp.LpVariable.dicts("number", (range(I), range(J)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum((distance[i][j] * price) * (number[i][j] / 2) for i in range(I) for j in range(J)), "Total Transportation Cost"

# Constraints
# Supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(number[i][j] for j in range(J)) <= numdepot[i], f"Supply_Depot_{i}"

# Demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(number[i][j] for i in range(I)) >= numport[j], f"Demand_Port_{j}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "number": [[pulp.value(number[i][j]) for j in range(J)] for i in range(I)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
output