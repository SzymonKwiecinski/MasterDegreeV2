import pulp

# Parse the input data
data = {
    "fixed_costs": [100, 150, 135],
    "additional_costs": [
        [10, 12, 20],
        [10, 8, 12],
        [15, 8, 20],
        [10, 6, 15],
        [8, 10, 15]
    ],
    "max_projects_per_consultant": 3
}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)
J = len(fixed_costs)

# Create a MILP problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision variables
x = [[pulp.LpVariable(f"x_{j}_{i}", cat='Binary') for i in range(I)] for j in range(J)]
y = [pulp.LpVariable(f"y_{j}", cat='Binary') for j in range(J)]

# Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] + pulp.lpSum(additional_costs[i][j] * x[j][i] for i in range(I)) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[j][i] for j in range(J)) == 1, f"Project_{i}_assign"

for j in range(J):
    problem += pulp.lpSum(x[j][i] for i in range(I)) <= K * y[j], f"MaxProjects_{j}"

# Solve the problem
problem.solve()

# Prepare output
assignments = [[int(x[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')