import pulp
import json

data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Define the problem
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Decision variables: number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(price * distance[i][j] * (x[i][j] / 2) for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Demand constraints for each port
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) == numport[j], f"Demand_Constraint_{j}"

# Supply constraints for each depot
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare the output
result = {
    "number": [[pulp.value(x[i][j]) for j in range(J)] for i in range(I)]
}

print(json.dumps(result))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')