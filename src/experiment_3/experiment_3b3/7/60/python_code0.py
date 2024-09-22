import pulp

# Data
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
I = len(additional_costs)
J = len(fixed_costs)

# Initialize the problem
problem = pulp.LpProblem("Project_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("ConsultantHired", range(J), cat='Binary')
assignment = pulp.LpVariable.dicts("ProjectAssignment", ((i, j) for i in range(I) for j in range(J)), cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * assignment[i, j] for i in range(I) for j in range(J))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignment[i, j] for j in range(J)) == 1, f"ProjectAssignment_{i}"

# A consultant can only be assigned projects if they are hired
for i in range(I):
    for j in range(J):
        problem += assignment[i, j] <= x[j], f"AssignOnlyIfHired_{i}_{j}"

# Each consultant can handle a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(assignment[i, j] for i in range(I)) <= K * x[j], f"MaxProjects_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')