import pulp

# Extract the data
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{k+1}", lowBound=0, cat='Continuous') for k in range(NumParts)]

# Objective function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumParts)])

# Constraints
for s in range(NumMachines):
    problem += pulp.lpSum([Time[k][s] * x[k] for k in range(NumParts)]) <= Capacity[s]

# Solve the problem
problem.solve()

# Print the results
for k in range(NumParts):
    print(f"Quantity of part {k+1}: {pulp.value(x[k])}")

print(f"Objective Value (Total Profit): <OBJ>{pulp.value(problem.objective)}</OBJ>")