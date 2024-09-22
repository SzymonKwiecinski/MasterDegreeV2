import pulp
import json

# Data from the provided JSON
data = json.loads('{"fixed_costs": [100, 150, 135], "additional_costs": [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], "max_projects_per_consultant": 3}')

# Problem definition
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the problem
problem = pulp.LpProblem("Project_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Hire", range(J), cat='Binary')  # Hiring decision for consultants
y = pulp.LpVariable.dicts("Assign", (range(I), range(J)), cat='Binary')  # Assignment decision

# Objective function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1, f"Project_Assignment_{i}"

# A consultant can only take on projects if they are hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j], f"Consultant_Hired_{i}_{j}"

# The total number of projects assigned to each consultant cannot exceed K
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= max_projects_per_consultant * x[j], f"Max_Projects_Consultant_{j}"

# Solve the problem
problem.solve()

# Output the assignments and the total cost
assignments = {f'Project_{i}': [j for j in range(J) if pulp.value(y[i][j]) == 1] for i in range(I)}
total_cost = pulp.value(problem.objective)

print("Assignments of projects to consultants:")
for project, consultants in assignments.items():
    print(f"{project}: {consultants}")

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')