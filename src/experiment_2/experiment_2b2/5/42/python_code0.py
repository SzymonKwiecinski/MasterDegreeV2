import pulp

# Given data
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

I = len(numdepot)
J = len(numport)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables x[i][j]: number of containers sent from depot i to port j
x = [[pulp.LpVariable(f'x_{i}_{j}', lowBound=0, cat='Integer') for j in range(J)] for i in range(I)]

# Objective function
problem += pulp.lpSum(x[i][j] * price * distance[i][j] / 2 for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Supply constraints: sum of containers sent from depot i should not exceed its supply
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand constraints: sum of containers received by port j should be exactly its demand
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output format
output = {
    "number": [[pulp.value(x[i][j]) for j in range(J)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')