import pulp

# Parse the input data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
costs = data['Cost']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute_processes = [pulp.LpVariable(f"Execute_Process_{l}", lowBound=0, cat='Continuous') for l in range(L)]

# Objective function: Maximize revenue
# Revenue per process = (product revenue - process cost) * number of times executed
revenue_terms = []
for l in range(L):
    revenue_from_process = 0
    for p in range(P):
        revenue_from_process += (output_matrix[l][p] * price[p])
    cost_of_process = costs[l]
    net_revenue_per_execute = revenue_from_process - cost_of_process
    revenue_terms.append(net_revenue_per_execute * execute_processes[l])

problem += pulp.lpSum(revenue_terms), "Total_Revenue"

# Constraints
# 1. Resource allocation constraints: Each crude oil allocation must not be exceeded
for i in range(O):
    problem += pulp.lpSum(execute_processes[l] * input_matrix[l][i] for l in range(L)) <= allocated[i], f"Crude_Resource_{i}"

# Solve the problem
problem.solve()

# Extract and print the solution
revenue = pulp.value(problem.objective)
execute = [pulp.value(execute_processes[l]) for l in range(L)]

output = {"revenue": revenue, "execute": execute}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')