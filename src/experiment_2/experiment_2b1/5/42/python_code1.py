import pulp
import json

# Input data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Number of depots and ports
I = len(numdepot)
J = len(numport)

# Create the problem
problem = pulp.LpProblem("Transport_Cost_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(price * distance[i][j] * (x[i, j] // 2) for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare output
result = {
    "number": [[x[i, j].varValue for j in range(J)] for i in range(I)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
print(json.dumps(result))