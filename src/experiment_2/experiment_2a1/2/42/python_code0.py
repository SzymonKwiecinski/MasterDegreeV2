import pulp
import json

# Input data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Problem parameters
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Define the problem
problem = pulp.LpProblem("Transportation_Cost_Minimization", pulp.LpMinimize)

# Decision variables: number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize the total transportation cost
problem += pulp.lpSum((distance[i][j] * price * (x[i, j] / 2)) for i in range(I) for j in range(J)), "Total_Transportation_Cost"

# Constraints

# Supply constraints for each depot
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_#{i}"

# Demand constraints for each port
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) == numport[j], f"Demand_Constraint_#{j}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "number": [[pulp.value(x[i, j]) for j in range(J)] for i in range(I)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')