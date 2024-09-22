import pulp
import json

# Data from the provided JSON format
data = json.loads("{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}")

# Parameters
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)       # number of consultants

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  # consultant hired
assignment = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')  # assignments

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * assignment[j][i] for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignment[j][i] for j in range(J)) == 1, f"Project_Assignment_{i}"

# Each consultant can be assigned up to K projects
for j in range(J):
    problem += pulp.lpSum(assignment[j][i] for i in range(I)) <= K * x[j], f"Consultant_Capacity_{j}"

# Relationship between assignment and hiring
for i in range(I):
    for j in range(J):
        problem += assignment[j][i] <= x[j], f"Assignment_Hiring_{j}_{i}"

# Solve the problem
problem.solve()

# Output the assignments and objective value
assignments = [[pulp.value(assignment[j][i]) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Print the results
print("Assignments of projects to consultants:")
for j in range(J):
    print(f'Consultant {j + 1}: ' + ', '.join(f'Project {i + 1} assigned' if pulp.value(assignment[j][i]) == 1 else f'Project {i + 1} not assigned' for i in range(I)))

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')