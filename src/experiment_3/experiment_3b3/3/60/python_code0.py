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
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)       # number of consultants

# Problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("HireConsultant", range(J), cat='Binary')
y = pulp.LpVariable.dicts("AssignProject", (range(I), range(J)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) +
    pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J))
)

# Constraints
# 1. Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1

# 2. A consultant can be assigned to up to K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= max_projects_per_consultant * x[j]

# 3. A project can only be assigned to a hired consultant
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j]

# Solve the problem
problem.solve()

# Assignments and total cost
assignments = [[int(y[i][j].varValue) for j in range(J)] for i in range(I)]
total_cost = pulp.value(problem.objective)

# Output
print(f'Assignments: {assignments}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')