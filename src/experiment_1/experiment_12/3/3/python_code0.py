import pulp

# Data
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

# Initialize the problem
problem = pulp.LpProblem("Spare_Part_Production", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(NumParts)]

# Objective function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(NumParts)), "Total Profit"

# Constraints
# Machine capacity constraints
for s in range(NumMachines):
    problem += (
        pulp.lpSum(Time[k][s] * x[k] for k in range(NumParts)) <= Capacity[s],
        f"Capacity_constraint_machine_{s}"
    )

# Solve the problem
problem.solve()

# Print the results
print(f"Status: {pulp.LpStatus[problem.status]}")
for k in range(NumParts):
    print(f"Quantity of spare part {k+1}: {pulp.value(x[k])}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")