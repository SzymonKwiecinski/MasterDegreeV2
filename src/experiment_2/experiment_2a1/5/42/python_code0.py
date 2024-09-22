import json
import pulp

# Data input
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 
        'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Extracting input data
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Define the number of depots and ports
I = len(numdepot)
J = len(numport)

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
# x[i][j] represents the number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("route", (range(I), range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(x[i][j] * (distance[i][j] * price) / 2 for i in range(I) for j in range(J))

# Constraints
# Supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_Depot_{i}"

# Demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j], f"Demand_Constraint_Port_{j}"

# Solve the problem
problem.solve()

# Prepare the output
output = {'number': [[int(x[i][j].varValue) for j in range(J)] for i in range(I)]}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')