import pulp

# Data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Extract data
num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Create a problem instance
problem = pulp.LpProblem("Maximize_Profits", pulp.LpMaximize)

# Decision variables: Quantity of spare parts to produce
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(num_parts)), "Total_Profit"

# Constraints
for s in range(num_machines):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(num_parts)) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')