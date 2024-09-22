import pulp
import numpy as np

# Data
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Parameters
I = len(data['numdepot'])  # Number of depots
J = len(data['numport'])    # Number of ports
price = data['price']
distance = np.array(data['distance'])

# Decision Variables
number = pulp.LpVariable.dicts("number", 
                                 ((i, j) for i in range(I) for j in range(J)), 
                                 lowBound=0, 
                                 cat='Integer')

# Problem Definition
problem = pulp.LpProblem("Container_Transport_Problem", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum((number[i, j] * price * distance[i, j]) for i in range(I) for j in range(J)) / 2

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= data['numdepot'][i]

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) == data['numport'][j]

# Non-negativity and integrality constraints
for i in range(I):
    for j in range(J):
        problem += number[i, j] >= 0
        problem += number[i, j] % 2 == 0  # number[i,j] must be an even integer

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')