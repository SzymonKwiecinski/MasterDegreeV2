import pulp
import json

# Input data
data_json = "{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}"
data = json.loads(data_json.replace("'", "\""))

# Problem definition
problem = pulp.LpProblem("OilRefineryOptimization", pulp.LpMaximize)

# Variables
execute = pulp.LpVariable.dicts("execute", range(data['L']), lowBound=0)

# Revenue Calculation
revenue = pulp.lpSum(execute[l] * (pulp.lpSum(data['Output'][l][p] * data['Price'][p] for p in range(data['P']))) for l in range(data['L']))

# Objective function
problem += revenue

# Constraints
for i in range(data['O']):
    problem += pulp.lpSum(execute[l] * data['Input'][l][i] for l in range(data['L'])) <= data['Allocated'][i]

# Solve the problem
problem.solve()

# Extract results
result_revenue = pulp.value(problem.objective)
execute_values = [execute[l].varValue for l in range(data['L'])]

# Output
output = {
    "revenue": result_revenue,
    "execute": execute_values
}

print(f' (Objective Value): <OBJ>{result_revenue}</OBJ>')