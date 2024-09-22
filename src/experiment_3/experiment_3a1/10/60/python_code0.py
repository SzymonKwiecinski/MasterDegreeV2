import pulp
import json

# Data from JSON format
data = json.loads("{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}")
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

# Indices
I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  # If consultant j is hired
y = pulp.LpVariable.dicts("y", (range(I), range(J)), cat='Binary')  # If project i is assigned to consultant j

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1

# A consultant can only work on a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j]

# A project can only be assigned if the corresponding consultant is hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j]

# Solve the problem
problem.solve()

# Output
assignments = {f'Consultant {j}': [] for j in range(J)}
for i in range(I):
    for j in range(J):
        if pulp.value(y[i][j]) == 1:
            assignments[f'Consultant {j}'].append(f'Project {i}')

total_cost = pulp.value(problem.objective)

print(f'Assignments: {assignments}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')