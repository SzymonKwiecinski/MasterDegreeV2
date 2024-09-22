import pulp

# Parse the input data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Define the number of products and machines
K = data['NumProducts']
S = data['NumMachines']

# Extract produce time, available time, and profit from data
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(K)])

# Constraints
for s in range(S):
    problem += pulp.lpSum([produce_time[k][s] * quantity[k] for k in range(K)]) <= available_time[s]

# Solve the LP problem
problem.solve()

# Prepare the output
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

# Display results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')