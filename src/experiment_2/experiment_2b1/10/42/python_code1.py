import pulp
import json

# Given data in JSON format
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 
        'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Extracting the problem parameters from the data
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']
I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables - number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum((distance[i][j] * price * (x[i][j] // 2)) for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_Depot_{i}"

# Demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j], f"Demand_Constraint_Port_{j}"

# Solve the problem
problem.solve()

# Prepare output
output = {"number": [[x[i][j].varValue for j in range(J)] for i in range(I)]}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
output