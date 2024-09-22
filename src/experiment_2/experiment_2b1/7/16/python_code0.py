import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Problem Parameters
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']
O = data['O']
P = data['P']
L = data['L']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables for each process execution
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0)

# Objective function: revenue - cost
revenue = pulp.lpSum((output_matrix[l][p] * price[p] * execute[l] for l in range(L) for p in range(P)))
total_cost = pulp.lpSum((cost[l] * execute[l] for l in range(L)))
problem += revenue - total_cost, "Total Revenue"

# Constraints for crude oil usage
for i in range(O):
    problem += pulp.lpSum((input_matrix[l][i] * execute[l] for l in range(L))) <= allocated[i], f"Crude_Usage_Constraint_{i}"

# Solve the problem
problem.solve()

# Gathering results
revenue_value = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

# Output result
output_result = {
    "revenue": revenue_value,
    "execute": execute_values
}
print(output_result)

# Print the objective value
print(f' (Objective Value): <OBJ>{revenue_value}</OBJ>')