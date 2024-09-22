import pulp

# Parse data
data = {
    'O': 2, 'P': 2, 'L': 3,
    'Allocated': [8000, 5000],
    'Price': [38, 33],
    'Input': [[3, 5], [1, 1], [5, 3]],
    'Output': [[4, 3], [1, 1], [3, 4]],
    'Cost': [51, 11, 40]
}

# Initialize the Problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision Variables
execute = [pulp.LpVariable(f"execute_{l+1}", lowBound=0, cat='Continuous') for l in range(data['L'])]

# Objective Function
revenue_terms = [
    sum(data['Output'][l][p] * data['Price'][p] * execute[l] for l in range(data['L']))
    for p in range(data['P'])
]
cost_terms = [
    data['Cost'][l] * sum(data['Output'][l][p] * execute[l] for p in range(data['P']))
    for l in range(data['L'])
]
problem += sum(revenue_terms) - sum(cost_terms)

# Constraints
# Crude oil allocation constraint for each type
for i in range(data['O']):
    problem += sum(data['Input'][l][i] * execute[l] for l in range(data['L'])) <= data['Allocated'][i]

# Solve the Problem
problem.solve()

# Outputs
revenue = pulp.value(problem.objective)
execution_values = [pulp.value(execute[l]) for l in range(data['L'])]

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')