import pulp
import json

data = json.loads('{"fixed_costs": [100, 150, 135], "additional_costs": [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], "max_projects_per_consultant": 3}')

# Extracting data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)      # Number of projects
J = len(fixed_costs)           # Number of consultants

# Create the problem
problem = pulp.LpProblem("Project_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  # Hiring decision for consultants
y = pulp.LpVariable.dicts("y", (range(I), range(J)), cat='Binary')  # Assignment of projects

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J)), "Total Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1, f"Assign_Project_{i}"

# A consultant can only work on a project if they are hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j], f"Consultant_Hired_{i}_{j}"

# Maximum projects assigned to each consultant
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= max_projects_per_consultant * x[j], f"Max_Projects_Consultant_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')