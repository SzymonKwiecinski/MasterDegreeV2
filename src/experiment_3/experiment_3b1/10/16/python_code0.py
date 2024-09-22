import pulp
import json

# Input data in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Extracting parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Define the problem
problem = pulp.LpProblem("OilRefineryProduction", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(1, L + 1), lowBound=0)

# Define the objective function
revenue = pulp.lpSum(price[p-1] * pulp.lpSum(output_matrix[l-1][p-1] * x[l] for l in range(1, L + 1)) for p in range(1, P + 1))
problem += revenue, "Total_Revenue"

# Define the constraints for crude oil allocation
for i in range(1, O + 1):
    problem += pulp.lpSum(input_matrix[l-1][i-1] * x[l] for l in range(1, L + 1)) <= allocated[i - 1], f"Crude_Oil_Allocation_{i}"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')