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

# Extract information from data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)    # Number of projects
J = len(fixed_costs)         # Number of consultants

# Create the optimization problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Define decision variables
assignments = pulp.LpVariable.dicts("assignment", 
                                     ((i, j) for i in range(I) for j in range(J)), 
                                     cat='Binary')

# Define the hiring variables
hired = pulp.LpVariable.dicts("hired", 
                               range(J), 
                               cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * hired[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * assignments[i, j] for i in range(I) for j in range(J))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[i, j] for j in range(J)) == 1

# Each consultant can only work on a limited number of projects
for j in range(J):
    problem += pulp.lpSum(assignments[i, j] for i in range(I)) <= max_projects_per_consultant * hired[j]

# Solve the problem
problem.solve()

# Collect assignments and total cost
assignments_result = [[int(assignments[i, j].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments_result,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')