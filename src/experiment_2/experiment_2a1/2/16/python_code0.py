import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Problem parameters
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

# Decision variables for the number of times to execute each process
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0, cat='Continuous')

# Objective function: Maximize revenue - cost
revenue = pulp.lpSum([(output_data[l][p] * execute[l] * price[p]) for l in range(L) for p in range(P)])
costs = pulp.lpSum([(cost[l] * execute[l]) for l in range(L)])
problem += revenue - costs, "Total_Profit"

# Constraints for raw materials
for i in range(O):
    problem += pulp.lpSum([input_data[l][i] * execute[l] for l in range(L)]) <= allocated[i], f"RawMaterialConstraint_{i}"

# Solve the problem
problem.solve()

# Output the results
revenue_value = pulp.value(problem.objective) + costs.value()  # Total revenue
execute_values = [pulp.value(execute[l]) for l in range(L)]

result = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')