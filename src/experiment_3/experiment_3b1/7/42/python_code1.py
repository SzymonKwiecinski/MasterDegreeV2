import pulp
import json

# Data in JSON format
data = json.loads("""
{"numdepot": [3, 3, 4], "numport": [1, 6, 3], "price": 3.0, "distance": [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}
""")

# Extracting data from the JSON
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Create the LP problem
problem = pulp.LpProblem("ContainerTransportation", pulp.LpMinimize)

# Decision Variables
number = pulp.LpVariable.dicts("number", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((number[i][j] / 2) * price * distance[i][j] for i in range(I) for j in range(J)), "TotalCost"

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(number[i][j] for j in range(J)) <= numdepot[i], f"SupplyConstraint_{i}"

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(number[i][j] for i in range(I)) >= numport[j], f"DemandConstraint_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')