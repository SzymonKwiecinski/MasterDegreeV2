import pulp
import json

# Data provided in JSON format.
data = json.loads('{"numdepot": [3, 3, 4], "numport": [1, 6, 3], "price": 3.0, "distance": [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}')

# Parameters
I = len(data['numdepot'])  # Number of depots
J = len(data['numport'])    # Number of ports
price = data['price']
distance = data['distance']
numdepot = data['numdepot']
numport = data['numport']

# Create the problem variable
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Continuous')
b = pulp.LpVariable.dicts("b", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(b[i][j] * price * distance[i][j] for i in range(I) for j in range(J)), "Total_Cost"

# Supply constraints
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j], f"Demand_Constraint_{j}"

# Barge constraints
for i in range(I):
    for j in range(J):
        problem += b[i][j] >= x[i][j] / 2, f"Barge_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')