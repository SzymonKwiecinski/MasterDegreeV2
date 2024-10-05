import pulp

# Data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Parameters
I = len(data['numdepot'])
J = len(data['numport'])
price = data['price']
distance = data['distance']
numdepot = data['numdepot']
numport = data['numport']

# Create the Linear Programming problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((1/2) * x[i][j] * price * distance[i][j] for i in range(I) for j in range(J)), "Total_Transportation_Cost"

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) == numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')