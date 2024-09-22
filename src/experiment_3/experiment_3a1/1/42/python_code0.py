import pulp
import json

# Data input in JSON format
data_json = "{'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}"
data = json.loads(data_json.replace("'", "\""))

# Extract parameters from data
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Number of depots and ports
I = len(numdepot)
J = len(numport)

# Create the problem
problem = pulp.LpProblem("Transporting_Containers", pulp.LpMinimize)

# Decision Variables
number = pulp.LpVariable.dicts("number", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((number[i][j] / 2) * distance[i][j] * price for i in range(I) for j in range(J)), "Total Transportation Cost"

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(number[i][j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(number[i][j] for i in range(I)) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the decision variables
for i in range(I):
    for j in range(J):
        print(f'number[{i+1},{j+1}] = {number[i][j].varValue}')