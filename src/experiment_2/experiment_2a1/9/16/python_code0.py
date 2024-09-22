import pulp
import json

# Input data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 
        'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 
        'Cost': [51, 11, 40]}

# Extract data from the input JSON
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables for how many times each process is executed
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0, cat='Continuous')

# Objective function: Maximize revenue - total cost
revenue = pulp.lpSum([execute[l] * pulp.lpSum([output_data[l][p] * price[p] for p in range(P)]) for l in range(L)])
total_cost = pulp.lpSum([execute[l] * cost[l] for l in range(L)])
problem += revenue - total_cost, "Total_Profit"

# Constraints for the available crude oil
for i in range(O):
    problem += pulp.lpSum([execute[l] * input_data[l][i] for l in range(L)]) <= allocated[i], f"Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
revenue_value = pulp.value(problem.objective) + total_cost  # since profit = revenue - cost
execute_values = [execute[l].varValue for l in range(L)]

# Format the output
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')