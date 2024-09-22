import pulp
import json

# Given data
data_json = '''{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}'''
data = json.loads(data_json)

# Define sets
projects = range(len(data['additional_costs']))  # Set of projects I
consultants = range(len(data['fixed_costs']))    # Set of consultants J

# Parameters
fixed_costs = data['fixed_costs']  # f_j
additional_costs = data['additional_costs']  # c_{i,j}
max_projects = data['max_projects_per_consultant']  # K

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("Hire", consultants, cat='Binary')  # x_j
y = pulp.LpVariable.dicts("Assign", (projects, consultants), cat='Binary')  # y_{i,j}

# Objective Function
problem += (pulp.lpSum(fixed_costs[j] * x[j] for j in consultants) + 
            pulp.lpSum(additional_costs[i][j] * y[i][j] for i in projects for j in consultants))

# Constraints
# Each project must be assigned to exactly one consultant
for i in projects:
    problem += (pulp.lpSum(y[i][j] for j in consultants) == 1)

# A consultant can only work on a project if they are hired
for i in projects:
    for j in consultants:
        problem += (y[i][j] <= x[j])

# Each consultant can be assigned a maximum of K projects
for j in consultants:
    problem += (pulp.lpSum(y[i][j] for i in projects) <= max_projects * x[j])

# Solve the problem
problem.solve()

# Output results
assignments = {j: [i for i in projects if pulp.value(y[i][j]) == 1] for j in consultants}
total_cost = pulp.value(problem.objective)

print(f'Assignments: {assignments}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')