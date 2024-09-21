import pulp

# Data from the provided json
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

NumParts = data['NumParts']
NumMachines = data['NumMachines']
Time = data['Time']
Profit = data['Profit']
Capacity = data['Capacity']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(NumParts)]

# Objective Function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumParts)]), "Total Profit"

# Constraints
# Machine capacity constraints
for s in range(NumMachines):
    problem += pulp.lpSum([Time[k][s] * x[k] for k in range(NumParts)]) <= Capacity[s], f"Capacity_Constraint_Machine_{s+1}"

# Solve the problem
problem.solve()

# Print the results
print("Solution Status:", pulp.LpStatus[problem.status])
for k in range(NumParts):
    print(f"Number of spare part {k+1} to produce: {pulp.value(x[k])}")

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')