import pulp
import json

# Load data
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Define parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Initialize the problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Process", range(1, L + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(price[p-1] * pulp.lpSum(output_matrix[l-1][p-1] * x[l] for l in range(1, L + 1)) for p in range(1, P + 1)) \
                - pulp.lpSum(cost[l-1] * pulp.lpSum(output_matrix[l-1][p-1] * x[l] for p in range(1, P + 1)) for l in range(1, L + 1))

# Constraints
for i in range(1, O + 1):
    problem += pulp.lpSum(input_matrix[l-1][i-1] * x[l] for l in range(1, L + 1)) <= allocated[i-1]

# Solve the problem
problem.solve()

# Output results
for l in range(1, L + 1):
    print(f'Process {l}: {x[l].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')