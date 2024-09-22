import pulp
import json

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
period = data['Period']
demand = data['Demand']

# Create the Linear Programming problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Variables: number of nurses starting on each day
start = pulp.LpVariable.dicts("start", range(1, 8), lowBound=0, cat='Integer')

# Objective: Minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(1, 8)), "Total_Nurses"

# Constraints: Ensure that the demand is met for each day
for j in range(1, 8):
    problem += (pulp.lpSum(start[(j - i) % 7 + 1] for i in range(period)) >= demand[j - 1]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Extracting results
start_values = [start[j].varValue for j in range(1, 8)]
total_nurses = pulp.value(problem.objective)

# Output results
output = {
    "start": start_values,
    "total": int(total_nurses)
}

# Print results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')