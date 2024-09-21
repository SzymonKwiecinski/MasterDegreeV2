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

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(NumParts)]

# Objective Function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(NumParts)), "Total_Profit"

# Constraints
# Machine capacity constraints
for s in range(NumMachines):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(NumParts)) <= Capacity[s], f"Capacity_Constraint_{s}"

# Solve
problem.solve()

# Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')