import pulp

# Data from the provided JSON
data = {
    'O': 2,
    'P': 2,
    'L': 3,
    'Allocated': [8000, 5000],
    'Price': [38, 33],
    'Input': [[3, 5], [1, 1], [5, 3]],
    'Output': [[4, 3], [1, 1], [3, 4]],
    'Cost': [51, 11, 40]
}

# Extracting data
O = data['O']
P = data['P']
L = data['L']
Allocated = data['Allocated']
Price = data['Price']
Input = data['Input']
Output = data['Output']
Cost = data['Cost']

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective Function
revenue = sum(Price[p] * sum(Output[l][p] * x[l] for l in range(L)) for p in range(P))
costs = sum(Cost[l] * sum(Output[l][p] * x[l] for p in range(P)) for l in range(L))
problem += revenue - costs

# Constraints
for i in range(O):
    problem += sum(Input[l][i] * x[l] for l in range(L)) <= Allocated[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')