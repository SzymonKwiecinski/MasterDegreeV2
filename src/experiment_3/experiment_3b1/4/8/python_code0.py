import pulp

# Data from JSON format
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Number of parts and machines
num_parts = data['NumParts']
num_machines = data['NumMachines']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(num_parts), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(num_parts)), "Total_Profit"

# Constraints for each machine
for s in range(num_machines):
    problem += pulp.lpSum(data['Time'][k][s] * x[k] for k in range(num_parts)) <= data['Capacity'][s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')