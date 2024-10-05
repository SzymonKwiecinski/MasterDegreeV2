import pulp

# Extracting data from json
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}
NumProducts = data['NumProducts']
NumMachines = data['NumMachines']
ProduceTime = data['ProduceTime']
AvailableTime = data['AvailableTime']
Profit = data['Profit']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(NumProducts)]

# Objective function: Maximize total profit
problem += pulp.lpSum(Profit[k] * quantity[k] for k in range(NumProducts))

# Constraints: Production time limits for each machine
for s in range(NumMachines):
    problem += pulp.lpSum(ProduceTime[k][s] * quantity[k] for k in range(NumProducts)) <= AvailableTime[s], f"Machine_{s}_Time"

# Solve the problem
problem.solve()

# Extract results
result = {
    "quantity": [pulp.value(quantity[k]) for k in range(NumProducts)]
}

# Print the results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')