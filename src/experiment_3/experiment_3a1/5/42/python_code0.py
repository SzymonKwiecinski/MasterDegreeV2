import pulp
import json

# Load data from the given JSON format
data_json = '''{'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}'''
data = json.loads(data_json.replace("'", "\""))

# Sets
I = range(len(data['numdepot']))
J = range(len(data['numport']))

# Parameters
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Decision Variables
number = pulp.LpVariable.dicts("number", (I, J), lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum((number[i][j] / 2) * distance[i][j] * price for i in I for j in J)

# Constraints
# Depot capacity constraints
for i in I:
    problem += pulp.lpSum(number[i][j] for j in J) <= numdepot[i]

# Port demand constraints
for j in J:
    problem += pulp.lpSum(number[i][j] for i in I) >= numport[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')