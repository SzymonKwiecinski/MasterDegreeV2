import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the LP Problem
problem = pulp.LpProblem("Oil_refinery_maximization", pulp.LpMaximize)

# Define decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Maximize revenue
revenue = pulp.lpSum([ (pulp.lpSum([(output_data[l][p] * execute[l] * price[p]) for l in range(L)]) - 
             (pulp.lpSum([cost[l] * execute[l] for l in range(L)])))
             for p in range(P)]) for l in range(L)])

# Set the objective
problem += revenue

# Constraints for allocated resources
for i in range(O):
    problem += pulp.lpSum([input_data[l][i] * execute[l] for l in range(L)]) <= allocated[i]

# Solve the problem
problem.solve()

# Calculate total revenue
total_revenue = pulp.value(problem.objective)
executions = [execute[l].varValue for l in range(L)]

# Output result
result = {
    "revenue": total_revenue,
    "execute": executions
}
print(result)
print(f' (Objective Value): <OBJ>{total_revenue}</OBJ>')