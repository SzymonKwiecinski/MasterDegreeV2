import pulp
import json

# Input data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Extract parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables for the number of times each process is executed
execute = pulp.LpVariable.dicts("Execute", range(L), lowBound=0, cat='Continuous')

# Objective function: Maximize total revenue - total cost
revenue = sum(execute[l] * (sum(output_data[l][p] * price[p] for p in range(P)) - cost[l]) for l in range(L))
problem += revenue

# Constraints for the crude oil allocation
for i in range(O):
    problem += (pulp.lpSum(execute[l] * input_data[l][i] for l in range(L)) <= allocated[i])

# Solve the problem
problem.solve()

# Get the results
total_revenue = pulp.value(problem.objective)
execute_results = [pulp.value(execute[l]) for l in range(L)]

# Output the results
output = {
    "revenue": total_revenue,
    "execute": execute_results
}

print(f' (Objective Value): <OBJ>{total_revenue}</OBJ>')