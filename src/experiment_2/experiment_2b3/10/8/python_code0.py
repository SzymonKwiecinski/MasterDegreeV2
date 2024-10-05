import pulp

# Extracting data from the provided JSON format
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

NumParts = data['NumParts']
NumMachines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(NumParts)]

# Objective function: Maximize total profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(NumParts)]), "Total Profit"

# Constraints for machine capacity
for s in range(NumMachines):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(NumParts)]) <= capacity[s], f"Capacity_Machine_{s}"

# Solve the problem
problem.solve()

# Output the results
solution = {
    "quantity": [pulp.value(quantity[k]) for k in range(NumParts)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')