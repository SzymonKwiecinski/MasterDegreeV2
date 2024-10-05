import pulp

# Extract data from JSON
data = {
    'NumProducts': 2, 
    'NumMachines': 2, 
    'ProduceTime': [[1, 3], [2, 1]], 
    'AvailableTime': [200, 100], 
    'Profit': [20, 10]
}

NumProducts = data['NumProducts']
NumMachines = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(NumProducts)]

# Define the objective function
problem += pulp.lpSum([profit[k] * quantities[k] for k in range(NumProducts)]), "Total Profit"

# Define constraints
for s in range(NumMachines):
    problem += pulp.lpSum([produce_time[k][s] * quantities[k] for k in range(NumProducts)]) <= available_time[s]

# Solve the problem
problem.solve()

# Retrieve the output
output = {
    "quantity": [pulp.value(quantities[k]) for k in range(NumProducts)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')