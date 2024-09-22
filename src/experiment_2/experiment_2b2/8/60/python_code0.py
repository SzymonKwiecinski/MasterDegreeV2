import pulp

# Data from the problem
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("assign", ((j, i) for j in range(J) for i in range(I)), cat='Binary')
y = pulp.LpVariable.dicts("hire", (j for j in range(J)), cat='Binary')

# Objective
problem += pulp.lpSum(fixed_costs[j] * y[j] + pulp.lpSum(additional_costs[i][j] * x[j, i] for i in range(I)) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[j, i] for j in range(J)) == 1, f"Project_{i}_assignment"

for j in range(J):
    problem += pulp.lpSum(x[j, i] for i in range(I)) <= max_projects_per_consultant * y[j], f"Max_projects_for_consultant_{j}"

# Solve
problem.solve()

# Prepare the output
assignments = [[pulp.value(x[j, i]) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')