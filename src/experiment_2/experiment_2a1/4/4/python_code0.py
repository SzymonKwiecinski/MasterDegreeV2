import pulp
import json

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(7)]

# Objective function: minimize the total number of nurses
problem += pulp.lpSum(start), "Total_Nurses"

# Constraints: ensure demand is met for each day
for j in range(7):
    problem += pulp.lpSum(start[(j - i) % 7] for i in range(period)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Extract results
start_values = [int(start[j].varValue) for j in range(7)]
total_nurses = int(pulp.value(problem.objective))

# Output result
output = {
    "start": start_values,
    "total": total_nurses
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')