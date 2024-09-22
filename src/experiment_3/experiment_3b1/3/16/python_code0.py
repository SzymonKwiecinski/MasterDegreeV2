import pulp

# Data from the provided JSON format
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

# Parameters
O = data['O']
P = data['P']
L = data['L']
Allocated = data['Allocated']
Price = data['Price']
Input = data['Input']
Output = data['Output']
Cost = data['Cost']

# Create a linear programming problem
problem = pulp.LpProblem("OilRefineryProduction", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("ProcessExecution", range(L), lowBound=0)

# Objective Function
problem += pulp.lpSum(Price[p] * pulp.lpSum(Output[l][p] * x[l] for l in range(L)) for p in range(P)), "TotalRevenue"

# Constraints
for i in range(O):
    problem += pulp.lpSum(Input[l][i] * x[l] for l in range(L)) <= Allocated[i], f"CrudeOilAvailability_{i}"

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print number of times each process should be executed
for l in range(L):
    print(f'Process {l}: {pulp.value(x[l])}')