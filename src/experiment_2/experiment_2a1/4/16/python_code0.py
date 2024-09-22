import pulp
import json

# Input data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Defining the problem
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Decision variables
execute = pulp.LpVariable.dicts("execute", range(data['L']), lowBound=0, cat='Continuous')

# Objective function: Maximize revenue
revenue = pulp.lpSum(
    (data['Price'][p] * pulp.lpSum(execute[l] * data['Output'][l][p] for l in range(data['L']))) 
    for p in range(data['P'])
) - pulp.lpSum(
    (execute[l] * data['Cost'][l] for l in range(data['L']))
)

problem += revenue

# Constraints for allocated crude oil
for i in range(data['O']):
    problem += pulp.lpSum(execute[l] * data['Input'][l][i] for l in range(data['L'])) <= data['Allocated'][i]

# Solving the problem
problem.solve()

# Extracting results
revenue_value = pulp.value(problem.objective)
execute_values = [execute[l].varValue for l in range(data['L'])]

# Output format
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{revenue_value}</OBJ>')