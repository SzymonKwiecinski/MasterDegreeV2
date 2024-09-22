import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)       # number of consultants

# Define the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')
y = pulp.LpVariable.dicts("hired", range(J), cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * x[j][i] for i in range(I) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[j][i] for j in range(J)) == 1  # Each project is assigned to exactly one consultant

for j in range(J):
    problem += pulp.lpSum(x[j][i] for i in range(I)) <= max_projects_per_consultant * y[j]  # A consultant can only handle up to K projects

# Solve the problem
problem.solve()

# Prepare the assignments and total cost
assignments = [[int(x[j][i].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output the result
result = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')