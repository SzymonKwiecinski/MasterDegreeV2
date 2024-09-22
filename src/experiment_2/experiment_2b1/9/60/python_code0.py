import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], 
                             [10, 8, 12], 
                             [15, 8, 20], 
                             [10, 6, 15], 
                             [8, 10, 15]], 
        'max_projects_per_consultant': 3}

# Problem parameters
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Define the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
assignments = pulp.LpVariable.dicts("assignment", (range(J), range(I)), 
                                     cat='Binary')  # assignment[j][i] = 1 if consultant j is assigned project i

# Objective function
total_cost = pulp.lpSum(fixed_costs[j] * pulp.lpSum(assignments[j][i] for i in range(I)) for j in range(J)) + \
                       pulp.lpSum(additional_costs[i][j] * assignments[j][i] for i in range(I) for j in range(J))
problem += total_cost

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[j][i] for j in range(J)) == 1, f"Project_{i}_assignment"

# Each consultant can handle a maximum number of projects
for j in range(J):
    problem += pulp.lpSum(assignments[j][i] for i in range(I)) <= max_projects_per_consultant, f"Consultant_{j}_max_projects"

# Solve the problem
problem.solve()

# Prepare the output
assignments_result = [[int(assignments[j][i].value()) for i in range(I)] for j in range(J)]
total_cost_value = pulp.value(problem.objective)

# Output the results
output = {
    "assignments": assignments_result,
    "total_cost": total_cost_value
}

print(json.dumps(output))  # Printing in JSON format
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')