import pulp
import json

# Data from the provided JSON format
data = json.loads('{"fixed_costs": [100, 150, 135], "additional_costs": [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], "max_projects_per_consultant": 3}')

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the linear programming problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), cat='Binary')  # x[i][j] = 1 if project i is assigned to consultant j
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')              # y[j] = 1 if consultant j is hired

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"Project_Assignment_{i}"

# A project can only be assigned to a hired consultant
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Assignment_to_Hired_Consultant_{i}_{j}"

# A consultant can be assigned up to a maximum number of projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= max_projects_per_consultant * y[j], f"Max_Projects_for_Consultant_{j}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')