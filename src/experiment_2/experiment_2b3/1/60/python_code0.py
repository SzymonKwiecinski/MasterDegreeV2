import pulp

# Data Input
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)  # number of consultants

# Problem Initialization
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("assign", [(j, i) for j in range(J) for i in range(I)], cat='Binary')
y = pulp.LpVariable.dicts("hire", [j for j in range(J)], cat='Binary')

# Objective Function
problem += pulp.lpSum(y[j] * fixed_costs[j] for j in range(J)) + pulp.lpSum(x[j, i] * additional_costs[i][j] for j in range(J) for i in range(I))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[j, i] for j in range(J)) == 1

# A consultant can handle at most K projects if hired
for j in range(J):
    problem += pulp.lpSum(x[j, i] for i in range(I)) <= max_projects_per_consultant * y[j]

# Solve the problem
problem.solve()

# Output Results
assignments = [[0 for _ in range(I)] for _ in range(J)]
for j in range(J):
    for i in range(I):
        assignments[j][i] = int(pulp.value(x[j, i]))

total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')