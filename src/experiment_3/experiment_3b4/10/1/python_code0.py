import pulp

# Parse data from the JSON structure
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0, cat=pulp.LpContinuous)

# Define the objective function
problem += pulp.lpSum([prices[j] * x[j] for j in range(M)])

# Define the constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * x[j] for j in range(M)]) <= available[i]

# Solve the problem
problem.solve()

# Print the outputs
print(f'Status: {pulp.LpStatus[problem.status]}')
for var in x.values():
    print(f'{var.name} = {var.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')