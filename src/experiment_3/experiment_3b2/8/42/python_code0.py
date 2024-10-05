import pulp
import json

# Load data
data = json.loads('{"numdepot": [3, 3, 4], "numport": [1, 6, 3], "price": 3.0, "distance": [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}')
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Set up the problem
I = len(numdepot)  # number of depots
J = len(numport)   # number of ports
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((x[i][j] / 2) * price * distance[i][j] for i in range(I) for j in range(J)), "Total Cost"

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')