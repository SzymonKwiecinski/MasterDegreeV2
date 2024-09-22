import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the LP problem
problem = pulp.LpProblem("Consultant_Allocation", pulp.LpMinimize)

# Decision variables
assignment = pulp.LpVariable.dicts("assignment", ((j, i) for j in range(J) for i in range(I)), cat='Binary')
consultant_hired = pulp.LpVariable.dicts("consultant_hired", (j for j in range(J)), cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * consultant_hired[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * assignment[(j, i)] for j in range(J) for i in range(I))

# Constraints
for i in range(I):
    problem += pulp.lpSum(assignment[(j, i)] for j in range(J)) == 1, f"Project_{i+1}_assigned"

for j in range(J):
    for i in range(I):
        problem += assignment[(j, i)] <= consultant_hired[j], f"Max_projects_for_consultant_{j+1}_for_project_{i+1}"

for j in range(J):
    problem += pulp.lpSum(assignment[(j, i)] for i in range(I)) <= K * consultant_hired[j], f"Consultant_{j+1}_max_projects"

# Solve the problem
problem.solve()

# Prepare output
assignments = [[assignment[(j, i)].value() for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output the result
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')