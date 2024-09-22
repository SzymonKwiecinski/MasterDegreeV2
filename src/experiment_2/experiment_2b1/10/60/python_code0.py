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

# Extract data from the input
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

# Problem setup
I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
assignments = pulp.LpVariable.dicts("assign", (range(J), range(I)), cat='Binary')
consultant_hired = pulp.LpVariable.dicts("hire", range(J), cat='Binary')

# Objective function
problem += (pulp.lpSum(fixed_costs[j] * consultant_hired[j] for j in range(J)) + 
             pulp.lpSum(additional_costs[i][j] * assignments[j][i] for i in range(I) for j in range(J)))

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[j][i] for j in range(J)) == 1

# Limit the number of projects per consultant
for j in range(J):
    problem += pulp.lpSum(assignments[j][i] for i in range(I)) <= max_projects_per_consultant * consultant_hired[j]

# Solve the problem
problem.solve()

# Output the results
assignments_result = [[int(assignments[j][i].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

result = {
    "assignments": assignments_result,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')