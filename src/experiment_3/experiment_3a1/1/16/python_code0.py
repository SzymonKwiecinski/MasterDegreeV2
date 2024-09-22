import pulp
import json

# Data provided in JSON format
data = {'O': 2, 'P': 2, 'L': 3, 
        'Allocated': [8000, 5000], 
        'Price': [38, 33], 
        'Input': [[3, 5], [1, 1], [5, 3]], 
        'Output': [[4, 3], [1, 1], [3, 4]], 
        'Cost': [51, 11, 40]}

# Extract the data from the input
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the linear programming problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(L), lowBound=0)

# Objective function
problem += pulp.lpSum(price[p] * pulp.lpSum(output_data[l][p] * x[l] for l in range(L)) for p in range(P)) - \
            pulp.lpSum(cost[l] * x[l] for l in range(L)), "Total_Profit"

# Constraints for crude oil availability
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * x[l] for l in range(L)) <= allocated[i], f"Crude_Oil_Availability_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')