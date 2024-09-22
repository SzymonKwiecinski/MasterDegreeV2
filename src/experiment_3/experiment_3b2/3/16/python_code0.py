import pulp
import json

# Data provided in JSON format
data = {'O': 2, 'P': 2, 'L': 3, 
        'Allocated': [8000, 5000], 
        'Price': [38, 33], 
        'Input': [[3, 5], [1, 1], [5, 3]], 
        'Output': [[4, 3], [1, 1], [3, 4]], 
        'Cost': [51, 11, 40]}

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, data['L'] + 1), lowBound=0, cat='Continuous')

# Objective Function
revenue_expression = pulp.lpSum(
    data['Output'][l-1][p-1] * data['Price'][p-1] * x[l]
    for l in range(1, data['L'] + 1)
    for p in range(1, data['P'] + 1)
    ) - pulp.lpSum(
    data['Cost'][l-1] * pulp.lpSum(data['Output'][l-1][p-1] * x[l] for p in range(1, data['P'] + 1))
    for l in range(1, data['L'] + 1)
)

problem += revenue_expression

# Constraints for crude oil allocation
for i in range(data['O']):
    problem += pulp.lpSum(data['Input'][l-1][i] * x[l] for l in range(1, data['L'] + 1)) <= data['Allocated'][i], f"Allocation_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')