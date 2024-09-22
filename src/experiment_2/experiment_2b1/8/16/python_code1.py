import json
import pulp

# Input data in JSON format
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 
        'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 
        'Cost': [51, 11, 40]}

# Number of crude types, products, and processes
O = data['O']
P = data['P']
L = data['L']

# Allocated crude oil, product prices, input/output and costs
allocated = data['Allocated']
price = data['Price']
inputs = data['Input']
outputs = data['Output']
costs = data['Cost']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables for each process execution
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0)

# Define the revenue function: Total revenue - Total cost
revenue = pulp.lpSum((outputs[l][p] * price[p] for l in range(L) for p in range(P)) * execute[l] for l in range(L)) - \
                     pulp.lpSum((costs[l] * execute[l] for l in range(L)))

# Set the objective function
problem += revenue

# Define the constraints based on crude oil allocations
for i in range(O):
    problem += pulp.lpSum(inputs[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_Allocation_{i}"

# Solve the problem
problem.solve()

# Gather the results
revenue_value = pulp.value(problem.objective)
execute_values = [execute[l].varValue for l in range(L)]

# Print the results
print(f' (Objective Value): <OBJ>{revenue_value}</OBJ>')
output = {
    "revenue": revenue_value,
    "execute": execute_values
}