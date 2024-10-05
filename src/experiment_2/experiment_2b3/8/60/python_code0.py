import pulp

# Data from JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [
        [10, 12, 20],
        [10, 8, 12],
        [15, 8, 20],
        [10, 6, 15],
        [8, 10, 15]
    ],
    'max_projects_per_consultant': 3
}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)      # number of consultants

# Problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("assignment", ((j, i) for j in range(J) for i in range(I)), cat='Binary')
y = pulp.LpVariable.dicts("hire", (j for j in range(J)), cat='Binary')

# Objective
problem += (
    pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) +
    pulp.lpSum(additional_costs[i][j] * x[j, i] for j in range(J) for i in range(I)),
    "Total Cost"
)

# Constraints
for i in range(I):
    problem += (pulp.lpSum(x[j, i] for j in range(J)) == 1, f"AssignProject_{i}")

for j in range(J):
    problem += (pulp.lpSum(x[j, i] for i in range(I)) <= K * y[j], f"MaxProjects_{j}")

# Solve
problem.solve()

# Output preparation
assignments = [[pulp.value(x[j, i]) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')