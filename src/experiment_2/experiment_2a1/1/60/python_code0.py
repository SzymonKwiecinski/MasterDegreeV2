import pulp
import json

# Input data
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Unpacking data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the problem variable
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision Variables
assignment = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')
consultant_used = pulp.LpVariable.dicts("consultant_used", range(J), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(fixed_costs[j] * consultant_used[j] for j in range(J)) +
    pulp.lpSum(additional_costs[i][j] * assignment[j][i] for i in range(I) for j in range(J))
)

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignment[j][i] for j in range(J)) == 1

# A consultant can only be assigned projects up to max_projects_per_consultant
for j in range(J):
    problem += pulp.lpSum(assignment[j][i] for i in range(I)) <= max_projects_per_consultant * consultant_used[j]

# Solve the problem
problem.solve()

# Prepare the output
assignments = [[int(assignment[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')