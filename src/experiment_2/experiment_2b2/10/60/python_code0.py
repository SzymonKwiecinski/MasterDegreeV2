import pulp

# Extracting data
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}
fixed_costs = data["fixed_costs"]
additional_costs = data["additional_costs"]
max_projects_per_consultant = data["max_projects_per_consultant"]

# Number of projects and consultants
I = len(additional_costs)
J = len(fixed_costs)

# Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
y = [pulp.LpVariable(f'y_{j}', cat='Binary') for j in range(J)]
x = [[pulp.LpVariable(f'x_{i}_{j}', cat='Binary') for j in range(J)] for i in range(I)]

# Objective function
problem += (pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) +
            pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J)))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1

for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= max_projects_per_consultant * y[j]

# Solve the problem
problem.solve()

# Prepare the solution
assignments = [[int(pulp.value(x[i][j])) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Print result in the specified format
output = {
    "assignments": assignments,
    "total_cost": total_cost
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')