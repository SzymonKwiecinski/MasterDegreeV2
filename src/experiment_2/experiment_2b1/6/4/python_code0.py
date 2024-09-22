import pulp
import json

# Data input from the provided JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables - number of nurses starting on each day
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function - minimize the total number of nurses hired
problem += pulp.lpSum(start), "Total_Nurses_Hired"

# Constraints to meet the demand for each day
for j in range(T):
    problem += (
        pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j],
        f"Demand_Constraint_{j}"
    )

# Solve the problem
problem.solve()

# Extract results
start_values = [int(var.varValue) for var in start]
total_nurses_hired = int(pulp.value(problem.objective))

# Output the result in the specified format
output = {
    "start": start_values,
    "total": total_nurses_hired
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# To return the output in the desired format
output