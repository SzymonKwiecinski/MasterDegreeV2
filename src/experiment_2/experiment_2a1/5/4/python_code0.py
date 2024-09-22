import pulp
import json

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables: start_j = number of nurses starting on day j
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(7)]

# Objective function: minimize the total number of hired nurses
problem += pulp.lpSum(start)

# Constraints: ensure enough nurses available for each day
for j in range(7):
    problem += pulp.lpSum(start[(j - i) % 7] for i in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Retrieve results
result_start = [int(start[j].value()) for j in range(7)]
total_nurses = int(pulp.value(problem.objective))

# Output results
output = {
    "start": result_start,
    "total": total_nurses
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')