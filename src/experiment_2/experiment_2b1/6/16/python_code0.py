import pulp
import json

# Input data in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Extracting data from input
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of times to execute each process
execute = [pulp.LpVariable(f"execute_{l}", lowBound=0) for l in range(L)]

# Objective function: Total revenue
revenue = pulp.lpSum([(output_data[l][p] * price[p] - cost[l]) * execute[l] for l in range(L) for p in range(P)])
problem += revenue

# Constraints for each crude oil type
for i in range(O):
    problem += pulp.lpSum([input_data[l][i] * execute[l] for l in range(L)]) <= allocated[i], f"Supply_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare the output
revenue_value = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')