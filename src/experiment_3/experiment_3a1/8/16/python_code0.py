import pulp
import json

# Data input in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Extracting data from JSON
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Initialize the problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Process", range(L), lowBound=0, cat='Continuous')

# Objective function
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_data[l][p] * x[l] for l in range(L)) for p in range(P))
costs = pulp.lpSum(cost[l] * pulp.lpSum(output_data[l][p] * x[l] for p in range(P)) for l in range(L))
problem += revenue - costs, "Total_Profit"

# Constraints
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * x[l] for l in range(L)) <= allocated[i], f"Crude_Allocation_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')