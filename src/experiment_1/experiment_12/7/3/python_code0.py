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

# Create a LP Maximization problem 
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x{k+1}", lowBound=0, cat='Continuous') for k in range(NumParts)]

# Objective Function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumParts)]), "Total_Profit"

# Constraints
for s in range(NumMachines):
    problem += pulp.lpSum([Time[k][s] * x[k] for k in range(NumParts)]) <= Capacity[s], f"Capacity_Constraint_Machine_{s+1}"

# Solve the problem
problem.solve()

# Output the solution and objective value
for k in range(NumParts):
    print(f"Quantity of spare part {k+1} to be produced: {x[k].varValue}")

print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")