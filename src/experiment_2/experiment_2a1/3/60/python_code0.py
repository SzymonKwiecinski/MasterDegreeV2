import json
import pulp

# Input data
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], 
                             [10, 8, 12], 
                             [15, 8, 20], 
                             [10, 6, 15], 
                             [8, 10, 15]], 
        'max_projects_per_consultant': 3}

# Define problem
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']  # Max projects per consultant

# Create the problem variable
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
assignments = pulp.LpVariable.dicts("assignment", 
                                     ((j, i) for j in range(J) for i in range(I)), 
                                     cat='Binary')
hire = pulp.LpVariable.dicts("hire", 
                              range(J), 
                              cat='Binary')

# Objective function
problem += (pulp.lpSum(data['fixed_costs'][j] * hire[j] for j in range(J)) + 
            pulp.lpSum(data['additional_costs'][i][j] * assignments[(j, i)] 
                       for i in range(I) for j in range(J)))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[(j, i)] for j in range(J)) == 1

# Each consultant can be assigned to a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(assignments[(j, i)] for i in range(I)) <= K * hire[j]

# Solve the problem
problem.solve()

# Collect the results
assignment_matrix = [[0 for _ in range(I)] for _ in range(J)]
for j in range(J):
    for i in range(I):
        assignment_matrix[j][i] = int(assignments[(j, i)].value())

total_cost = pulp.value(problem.objective)

# Prepare output
output = {
    "assignments": assignment_matrix,
    "total_cost": total_cost
}

# Print result
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')