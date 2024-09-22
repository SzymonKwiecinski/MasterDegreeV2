import pulp

# Data from the problem
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

num_projects = len(additional_costs)
num_consultants = len(fixed_costs)

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Assign", ((j, i) for j in range(num_consultants) for i in range(num_projects)), cat='Binary')
y = pulp.LpVariable.dicts("Hire", (j for j in range(num_consultants)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(fixed_costs[j] * y[j] for j in range(num_consultants)) +
    pulp.lpSum(additional_costs[i][j] * x[j, i] for j in range(num_consultants) for i in range(num_projects))
)

# Constraints
# Each project is assigned to exactly one consultant
for i in range(num_projects):
    problem += pulp.lpSum(x[j, i] for j in range(num_consultants)) == 1

# A consultant must be hired if they are assigned any project
for j in range(num_consultants):
    for i in range(num_projects):
        problem += x[j, i] <= y[j]

# A consultant can be assigned at most K projects
for j in range(num_consultants):
    problem += pulp.lpSum(x[j, i] for i in range(num_projects)) <= K

# Solve the problem
problem.solve()

# Prepare the output
assignments = [[pulp.value(x[j, i]) for i in range(num_projects)] for j in range(num_consultants)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')