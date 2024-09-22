import pulp
import json

# Data from the provided JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("NurseScheduling", pulp.LpMinimize)

# Decision variables: start_j for each day j
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize the total number of nurses hired
problem += pulp.lpSum(start), "TotalNursesHired"

# Constraints to meet demand for each day
for j in range(T):
    problem += (pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j], f'DemandConstraint_{j}')

# Solve the problem
problem.solve()

# Prepare output
output = {
    "start": [start[j].varValue for j in range(T)],
    "total": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the output
print(json.dumps(output))