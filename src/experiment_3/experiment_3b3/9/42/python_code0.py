import pulp

# Data from the input
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Constants
I = len(data['numdepot'])
J = len(data['numport'])

# Problem definition
problem = pulp.LpProblem("Transporting_Containers", pulp.LpMinimize)

# Decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), 
                               lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((number[i, j] / 2) * data['distance'][i][j] * data['price'] 
                      for i in range(I) for j in range(J)), "Total_Transportation_Cost"

# Constraints
# Supply constraints
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= data['numdepot'][i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= data['numport'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Extract the number values in the required format
number_values = [[pulp.value(number[i, j]) for i in range(I)] for j in range(J)]

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print({"number": number_values})