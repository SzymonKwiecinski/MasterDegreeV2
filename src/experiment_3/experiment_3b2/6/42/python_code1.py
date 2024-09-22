import pulp
import json

# Data input
data = json.loads('{"numdepot": [3, 3, 4], "numport": [1, 6, 3], "price": 3.0, "distance": [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}')
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Number of depots and ports
I = len(numdepot)
J = len(numport)

# Create the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), 
                               lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum((x[i, j] * price * distance[i][j]) / 2 for i in range(I) for j in range(J)), "Total_Cost"

# Supply constraints
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) == numport[j], f"Demand_Constraint_{j}"

# Integer and non-negativity constraints (enforcing multiples of 2)
for i in range(I):
    for j in range(J):
        problem += x[i, j] % 2 == 0, f"Integer_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')