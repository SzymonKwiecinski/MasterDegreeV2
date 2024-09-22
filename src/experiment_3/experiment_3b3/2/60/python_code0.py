import pulp

# Data provided
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

# Extracting data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

# Number of projects (I) and consultants (J)
I = len(additional_costs)
J = len(fixed_costs)

# Create the LP problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', cat='Binary') for j in range(J)]
y = [[pulp.LpVariable(f'y_{i}_{j}', cat='Binary') for j in range(J)] for i in range(I)]

# Objective function
problem += (
    pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) +
    pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J))
), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1, f"Project_Assignment_{i}"

# A consultant can be assigned to a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= max_projects_per_consultant * x[j], f"Max_Projects_Consultant_{j}"

# Solve the problem
problem.solve()

# Output results
assignments = [[int(y[i][j].varValue) for j in range(J)] for i in range(I)]
total_cost = pulp.value(problem.objective)

print(f'(Objective Value): <OBJ>{total_cost}</OBJ>')