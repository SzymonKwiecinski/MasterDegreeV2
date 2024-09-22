import pulp

# Problem Data
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
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the MILP problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision Variables
y = pulp.LpVariable.dicts("hire_consultant", range(J), cat='Binary')
x = pulp.LpVariable.dicts("assign_project", ((i, j) for i in range(I) for j in range(J)), cat='Binary')

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * x[(i, j)] for i in range(I) for j in range(J))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[(i, j)] for j in range(J)) == 1

# A consultant can be assigned a project only if they are hired
for j in range(J):
    for i in range(I):
        problem += x[(i, j)] <= y[j]

# Each consultant can take up to K projects
for j in range(J):
    problem += pulp.lpSum(x[(i, j)] for i in range(I)) <= max_projects_per_consultant

# Solve the problem
problem.solve()

# Prepare output data
assignments = [[int(x[(i, j)].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

print({
    "assignments": assignments,
    "total_cost": total_cost
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')