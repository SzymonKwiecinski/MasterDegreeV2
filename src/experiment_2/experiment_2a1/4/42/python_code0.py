import pulp
import json

data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Create the problem variable
problem = pulp.LpProblem("TransportationCostMinimization", pulp.LpMinimize)

# Decision variables for the number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum([x[i, j] * price * distance[i][j] / 2 for i in range(I) for j in range(J)]), "TotalCost"

# Constraints for supplies (depot capacity)
for i in range(I):
    problem += pulp.lpSum([x[i, j] for j in range(J)]) <= numdepot[i], f"SupplyConstraintDepot_{i}"

# Constraints for demands (port requirement)
for j in range(J):
    problem += pulp.lpSum([x[i, j] for i in range(I)]) >= numport[j], f"DemandConstraintPort_{j}"

# Solve the problem
problem.solve()

# Prepare the output
result = {
    "number": [[pulp.value(x[i, j]) for j in range(J)] for i in range(I)]
}

# Printing objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')