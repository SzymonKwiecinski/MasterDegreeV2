import pulp
import json

# Load the data from the given format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Variables for the number of nurses starting their shift on each day
start = pulp.LpVariable.dicts("start", range(1, data['T'] + 1), lowBound=0, cat='Integer')

# Objective function: Minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(1, data['T'] + 1)), "Total_Nurses"

# Constraints: Ensure demand is met for each day
for j in range(1, data['T'] + 1):
    problem += (
        pulp.lpSum(start[(j - k) % data['T'] + 1] for k in range(period)) >= demand[j - 1],
        f"Demand_Constraint_day_{j}"
    )

# Solve the problem
problem.solve()

# Prepare the output
start_values = [int(start[j].varValue) for j in range(1, data['T'] + 1)]
total_nurses = int(pulp.value(problem.objective))

# Print the results
output = {
    "start": start_values,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')