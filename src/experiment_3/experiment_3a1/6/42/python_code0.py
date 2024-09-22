import pulp
import json

# Load data from JSON format
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Initialize the problem
problem = pulp.LpProblem("Container_Transport_Problem", pulp.LpMinimize)

# Define indices
I = len(data['numdepot'])  # Number of depots
J = len(data['numport'])    # Number of ports

# Decision variables
number = pulp.LpVariable.dicts("number", [(i, j) for i in range(I) for j in range(J)], lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((number[i, j] / 2) * data['distance'][i][j] * data['price'] for i in range(I) for j in range(J)), "Total_Transport_Cost"

# Supply constraints at depots
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= data['numdepot'][i], f"Supply_Constraint_Depot_{i}"

# Demand constraints at ports
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= data['numport'][j], f"Demand_Constraint_Port_{j}"

# Solve the problem
problem.solve()

# Prepare output format
output = {
    "number": [[pulp.value(number[i, j]) for i in range(I)] for j in range(J)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Optional: Print the distribution of containers
print(json.dumps(output, indent=4))