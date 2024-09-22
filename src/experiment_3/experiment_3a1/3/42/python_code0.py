import pulp
import json

# Given data in JSON format
data = json.loads('{"numdepot": [3, 3, 4], "numport": [1, 6, 3], "price": 3.0, "distance": [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}')

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Initialize the LP problem
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Define indices
I = len(numdepot)
J = len(numport)

# Define decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((number[i, j] / 2) * distance[i][j] * price for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Constraints for the supply at each depot
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_Depot_{i+1}"

# Constraints for the demand at each port
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= numport[j], f"Demand_Constraint_Port_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')