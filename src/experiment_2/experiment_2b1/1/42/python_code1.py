import json
import pulp

# Input data from the provided JSON format
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables: number of containers sent from depot i to port j
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective function: Minimize the total transportation cost
problem += pulp.lpSum((distance[i][j] * price * (x[i][j] / 2)) for i in range(I) for j in range(J)), "Total_Transportation_Cost"

# Constraints for depots
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"Depot_{i}_Capacity"

# Constraints for ports
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j], f"Port_{j}_Demand"

# Solve the problem
problem.solve()

# Prepare the output
result = {
    "number": [[pulp.value(x[i][j]) for j in range(J)] for i in range(I)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')