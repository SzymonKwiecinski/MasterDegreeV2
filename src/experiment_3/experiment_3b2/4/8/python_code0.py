import pulp

# Data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Define the problem
problem = pulp.LpProblem("Spare_Automobile_Parts_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, data['NumParts'] + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Profit'][k-1] * x[k] for k in range(1, data['NumParts'] + 1)), "Total_Profit"

# Capacity constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['Time'][k-1][s] * x[k] for k in range(1, data['NumParts'] + 1)) <= data['Capacity'][s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')