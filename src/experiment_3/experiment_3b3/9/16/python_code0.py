import pulp

# Data input
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

# Initialize the problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision Variables
execute_vars = [pulp.LpVariable(f'execute_{l+1}', lowBound=0, cat='Continuous') for l in range(data['L'])]

# Objective Function
revenue = (
    pulp.lpSum(data['Price'][p] * pulp.lpSum(data['Output'][l][p] * execute_vars[l] for l in range(data['L'])) for p in range(data['P'])) -
    pulp.lpSum(data['Cost'][l] * pulp.lpSum(data['Output'][l][p] * execute_vars[l] for p in range(data['P'])) for l in range(data['L']))
)
problem += revenue

# Constraints
for i in range(data['O']):
    problem += (pulp.lpSum(data['Input'][l][i] * execute_vars[l] for l in range(data['L'])) <= data['Allocated'][i])

# Solve the problem
problem.solve()

# Output the results
execute_values = [pulp.value(var) for var in execute_vars]
revenue = pulp.value(problem.objective)

print("Optimal execute values:", execute_values)
print(f"Total Revenue (Objective Value): <OBJ>{revenue}</OBJ>")