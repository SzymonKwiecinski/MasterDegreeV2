import pulp

# Data from JSON
data = {
    'O': 2, 
    'P': 2, 
    'L': 3, 
    'Allocated': [8000, 5000], 
    'Price': [38, 33], 
    'Input': [[3, 5], [1, 1], [5, 3]], 
    'Output': [[4, 3], [1, 1], [3, 4]], 
    'Cost': [51, 11, 40]
}

# Extracting the data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_ = data['Input']
output = data['Output']
cost = data['Cost']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective Function
revenue = pulp.lpSum((price[p] * output[l][p] - cost[l]) * execute[l] for l in range(L) for p in range(P))
problem += revenue, "Total_Revenue"

# Constraints: Crude oil availability
for i in range(O):
    problem += pulp.lpSum(input_[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_Oil_{i}_Constraint"

# Solve the problem
problem.solve()

# Prepare the results
objective_value = pulp.value(problem.objective)
execution_plan = [pulp.value(execute[l]) for l in range(L)]

# Output the results
results = {
    "revenue": objective_value,
    "execute": execution_plan
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')