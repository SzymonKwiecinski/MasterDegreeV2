import pulp
import json

# Load data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Parameters
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # number of depots
J = len(numport)   # number of ports

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[i, j] * (price * distance[i][j]) for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Supply constraints
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare output
result = [[pulp.value(x[i, j]) for j in range(J)] for i in range(I)]
output = {"number": result}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')