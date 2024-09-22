import pulp
import json

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("NurseScheduling", pulp.LpMinimize)

# Decision variables
start = pulp.LpVariable.dicts("start", range(data['T']), lowBound=0, cat='Integer')

# Objective function: Minimize total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(data['T'])), "TotalNurses"

# Constraints
for j in range(data['T']):
    problem += (
        pulp.lpSum(start[(j - i) % data['T']] for i in range(period)) >= demand[j],
        f"DemandConstraint_{j}",
    )

# Solve the problem
problem.solve()

# Collect results
result_start = [start[j].varValue for j in range(data['T'])]
total_nurses = pulp.value(problem.objective)

# Output format
output = {
    "start": result_start,
    "total": total_nurses,
}

# Print results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')