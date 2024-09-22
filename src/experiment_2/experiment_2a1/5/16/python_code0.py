import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Extracting data from the JSON-like structure
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables for each process
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(data['L'])]

# Objective function: Maximize total revenue
revenue = pulp.lpSum([(pulp.lpSum([output_data[l][p] * execute[l] for l in range(data['L'])]) * price[p] for p in range(data['P'])]) - 
                       (pulp.lpSum([cost[l] * execute[l] for l in range(data['L'])])) for l in range(data['L'])])
problem += revenue

# Constraints for each type of crude oil
for i in range(data['O']):
    problem += (pulp.lpSum([input_data[l][i] * execute[l] for l in range(data['L'])]) <= allocated[i], f"oil_constraint_{i}")

# Solve the problem
problem.solve()

# Prepare the output
total_revenue = pulp.value(problem.objective)
execution_plan = [pulp.value(execute[l]) for l in range(data['L'])]

# Output the results
output_result = {
    "revenue": total_revenue,
    "execute": execution_plan
}

print(output_result)
print(f' (Objective Value): <OBJ>{total_revenue}</OBJ>')