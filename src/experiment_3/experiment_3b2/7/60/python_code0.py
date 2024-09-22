import pulp

# Data from JSON format
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Number of projects and consultants
I = len(data['additional_costs'])
J = len(data['fixed_costs'])
K = data['max_projects_per_consultant']

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), cat='Binary')  # Project i assigned to Consultant j
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')  # Consultant j hired

# Objective Function
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J)), "Total_Cost"

# Constraints

# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"One_consultant_per_project_{i}"

# A consultant can be assigned at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j], f"Max_projects_per_consultant_{j}"

# If a project is assigned to a consultant, then consultant must be hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Hire_consultant_if_assigned_{i}_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')