import pulp

# Data from the provided JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Parameters
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']  # Maximum projects per consultant

# Create the linear programming problem
problem = pulp.LpProblem("Consultant_Selection", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("project_assignment", (range(I), range(J)), cat='Binary')
y = pulp.LpVariable.dicts("consultant_hired", range(J), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['fixed_costs'][j] * y[j] for j in range(J)) + \
           pulp.lpSum(data['additional_costs'][i][j] * x[i][j] for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"Project_Assignment_{i}"

# If a project is assigned to a consultant, that consultant must be hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Consultant_Hire_{i}_{j}"

# Each consultant can be assigned at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j], f"Max_Projects_Consultant_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')