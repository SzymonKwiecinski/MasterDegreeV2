import pulp

# Given data
data = {
    "numdepot": [3, 3, 4],
    "numport": [1, 6, 3],
    "price": 3.0,
    "distance": [
        [0.0, 2.0, 5.0],
        [2.0, 0.0, 3.0],
        [5.0, 3.0, 0.0]
    ]
}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Define the problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
containers = pulp.LpVariable.dicts("Containers",
                                   ((i, j) for i in range(I) for j in range(J)),
                                   lowBound=0,
                                   cat='Integer')

# Objective function
problem += pulp.lpSum((distance[i][j] * price * 0.5) * containers[(i, j)] for i in range(I) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(containers[(i, j)] for j in range(J)) <= numdepot[i], f"Depot_{i}_Supply"

for j in range(J):
    problem += pulp.lpSum(containers[(i, j)] for i in range(I)) >= numport[j], f"Port_{j}_Demand"

# Solve the problem
problem.solve()

# Prepare the output
number = [[containers[(i, j)].varValue for j in range(J)] for i in range(I)]
output = {"number": number}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')