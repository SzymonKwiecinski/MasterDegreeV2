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

I = len(additional_costs)
J = len(fixed_costs)

# Problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Assignment", ((j, i) for j in range(J) for i in range(I)), cat='Binary')
y = pulp.LpVariable.dicts("Consultant", (j for j in range(J)), cat='Binary')

# Objective function
problem += pulp.lpSum(y[j] * fixed_costs[j] for j in range(J)) + pulp.lpSum(x[j, i] * additional_costs[i][j] for j in range(J) for i in range(I))

# Constraints

# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[j, i] for j in range(J)) == 1

# Each consultant can handle at most K projects
for j in range(J):
    problem += pulp.lpSum(x[j, i] for i in range(I)) <= K * y[j]

# Solve
problem.solve()

# Prepare the output
assignments = [[int(x[j, i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(output)