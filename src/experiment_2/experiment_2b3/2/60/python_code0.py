import pulp

data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)
J = len(fixed_costs)

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')
y = pulp.LpVariable.dicts("hire", range(J), cat='Binary')

# Objective function
problem += pulp.lpSum([fixed_costs[j] * y[j] for j in range(J)]) + \
           pulp.lpSum([additional_costs[i][j] * x[j][i] for j in range(J) for i in range(I)])

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum([x[j][i] for j in range(J)]) == 1

# Each consultant can handle at most `max_projects_per_consultant` projects
for j in range(J):
    problem += pulp.lpSum([x[j][i] for i in range(I)]) <= max_projects_per_consultant

# A consultant can only be assigned a project if they are hired
for j in range(J):
    for i in range(I):
        problem += x[j][i] <= y[j]

# Solve the problem
problem.solve()

# Extract solution
assignments = [[pulp.value(x[j][i]) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')