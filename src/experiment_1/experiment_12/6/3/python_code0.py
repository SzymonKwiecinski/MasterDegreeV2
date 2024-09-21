import pulp

# Data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [
        [2, 3],  # Time for part 1 on machines 1 and 2
        [1, 2],  # Time for part 2 on machines 1 and 2
        [3, 2],  # Time for part 3 on machines 1 and 2
        [3, 1],  # Time for part 4 on machines 1 and 2
        [1, 1],  # Time for part 5 on machines 1 and 2
    ],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

NumParts = data['NumParts']
NumMachines = data['NumMachines']
Time = data['Time']
Profit = data['Profit']
Capacity = data['Capacity']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(NumParts), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(NumParts)), "Total Profit"

# Constraints
# Machine capacity constraints
for s in range(NumMachines):
    problem += (pulp.lpSum(Time[k][s] * x[k] for k in range(NumParts)) <= Capacity[s], f"Capacity_Constraint_Machine_{s+1}")

# Solve the problem
problem.solve()

# Results
print("Status:", pulp.LpStatus[problem.status])
for k in range(NumParts):
    print(f"Quantity of spare part {k+1} to be produced:", pulp.value(x[k]))

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')