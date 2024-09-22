import pulp
import json

# Input data
data = {'O': 2, 'P': 2, 'L': 3, 
        'Allocated': [8000, 5000], 
        'Price': [38, 33], 
        'Input': [[3, 5], [1, 1], [5, 3]], 
        'Output': [[4, 3], [1, 1], [3, 4]], 
        'Cost': [51, 11, 40]}

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables: Number of times to execute each process
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(data['L'])]

# Objective function: Maximize the total revenue - total costs
revenue_expr = sum(execute[l] * (sum(data['Price'][p] * data['Output'][l][p] for p in range(data['P']))) for l in range(data['L']))
cost_expr = sum(execute[l] * data['Cost'][l] for l in range(data['L']))
problem += revenue_expr - cost_expr

# Constraints: Input constraints for each crude oil type
for i in range(data['O']):
    problem += (sum(execute[l] * data['Input'][l][i] for l in range(data['L'])) <= data['Allocated'][i], f"Input_Constraint_{i}")

# Solve the problem
problem.solve()

# Prepare the output
revenue = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(data['L'])]

# Print results
print(f' (Objective Value): <OBJ>{revenue}</OBJ>')
print(json.dumps({"revenue": revenue, "execute": execute_values}))