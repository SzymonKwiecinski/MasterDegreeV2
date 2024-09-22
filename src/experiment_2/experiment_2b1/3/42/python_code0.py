import pulp
import json

# Input Data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Define the LP problem
problem = pulp.LpProblem("Transport_Containers", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(x[i, j] * (price * distance[i][j]) / 2 for i in range(I) for j in range(J)), "Total_Transportation_Cost"

# Constraints
# Supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_depot_{i}"

# Demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j], f"Demand_Constraint_port_{j}"

# Solve the problem
problem.solve()

# Prepare the result
result = {
    "number": [[pulp.value(x[i, j]) for j in range(J)] for i in range(I)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print result
print(json.dumps(result))