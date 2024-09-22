import json
import pulp

data = json.loads("<DATA>{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>")

# Extracting inputs from data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute = pulp.LpVariable.dicts("Execute", range(L), lowBound=0, cat='Continuous')

# Objective function: Maximize revenue
revenue = pulp.lpSum((output_data[l][p] * price[p] for l in range(L) for p in range(P))) \
                     * execute[l] - pulp.lpSum(cost[l] * execute[l] for l in range(L))

problem += revenue

# Constraints
# Allocate constraints for each crude oil type
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * execute[l] for l in range(L)) <= allocated[i], f"AllocConstraint_{i}"

# Solve the problem
problem.solve()

# Get the results
revenue_value = pulp.value(problem.objective)
execute_values = [execute[l].varValue for l in range(L)]

# Output result
result = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')