import pulp

# Parse data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [
        [0.0, 2.0, 5.0],
        [2.0, 0.0, 3.0],
        [5.0, 3.0, 0.0]
    ]
}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Indices
I = len(numdepot)
J = len(numport)

# Create LP problem
problem = pulp.LpProblem("ContainerTransport", pulp.LpMinimize)

# Define decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), 
                                   lowBound=0, cat=pulp.LpInteger)

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(price * distance[i][j] * (number[(i, j)] / 2.0) for i in range(I) for j in range(J)), "TotalCost"

# Constraints for supply: Containers sent from each depot should not exceed available containers
for i in range(I):
    problem += pulp.lpSum(number[(i, j)] for j in range(J)) <= numdepot[i], f"DepotSupply_{i}"

# Constraints for demand: Containers received at each port should meet the required containers
for j in range(J):
    problem += pulp.lpSum(number[(i, j)] for i in range(I)) >= numport[j], f"PortDemand_{j}"

# Solve the problem
problem.solve()

# Output solution
solution = {
    "number": [[pulp.value(number[(i, j)]) for i in range(I)] for j in range(J)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')