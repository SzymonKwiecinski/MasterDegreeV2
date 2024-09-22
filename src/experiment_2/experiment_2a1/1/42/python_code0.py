import pulp
import json

data = json.loads("<DATA>{'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}</DATA>")

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables: number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Integer')

# Objective function: Minimize total cost
problem += pulp.lpSum((x[i][j] / 2) * distance[i][j] * price for i in range(I) for j in range(J))

# Constraints
# 1. Supply constraints: The total number of containers sent from each depot should not exceed its availability
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i]

# 2. Demand constraints: The total number of containers received at each port should meet its demand
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) == numport[j]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "number": [[x[i][j].varValue for j in range(J)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')