import pulp
import json

# Data from JSON format
data = {
    'fixed_costs': [100, 150, 135], 
    'additional_costs': [
        [10, 12, 20], 
        [10, 8, 12], 
        [15, 8, 20], 
        [10, 6, 15], 
        [8, 10, 15]
    ], 
    'max_projects_per_consultant': 3
}

# Parameters
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']
f = data['fixed_costs']
c = data['additional_costs']

# Decision Variables
x = pulp.LpVariable.dicts('x', range(J), cat='Binary')  # consultant hired
y = pulp.LpVariable.dicts('y', (range(I), range(J)), cat='Binary')  # project assigned to consultant

# Problem definition
problem = pulp.LpProblem("Consultant_Project_Assignment", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(f[j] * x[j] for j in range(J)) + pulp.lpSum(c[i][j] * y[i][j] for i in range(I) for j in range(J))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1

# A consultant can be assigned a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j]

# Solve the problem
problem.solve()

# Output the assignments and total cost
assignments = {(j, i): pulp.value(y[i][j]) for i in range(I) for j in range(J)}
total_cost = pulp.value(problem.objective)

print(f'Assignments: {assignments}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')