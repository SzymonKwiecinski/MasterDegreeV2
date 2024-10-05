import pulp

# Data from the provided JSON format
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Initialize the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(data['NumParts']), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(data['NumParts'])), "Total_Profit"

# Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['Time'][k][s] * quantity[k] for k in range(data['NumParts'])) <= data['Capacity'][s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')