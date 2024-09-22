import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

# Extracting values from data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

# Number of consultants and projects
J = len(fixed_costs)
I = len(additional_costs)

# Problem definition
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(J), range(I)), cat='Binary')  # Assignment variables
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')  # Consultant hiring variables

# Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * x[j][i] for j in range(J) for i in range(I))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[j][i] for j in range(J)) == 1  # Each project is assigned to one consultant

for j in range(J):
    problem += pulp.lpSum(x[j][i] for i in range(I)) <= max_projects_per_consultant * y[j]  # Up to K projects per consultant

# Solve the problem
problem.solve()

# Prepare output
assignments = [[int(x[j][i].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

# Print objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')