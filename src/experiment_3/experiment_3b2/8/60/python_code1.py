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

# Define sets
I = range(len(data['additional_costs']))  # Projects
J = range(len(data['fixed_costs']))        # Consultants

# Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (I, J), cat='Binary')  # Assignment variables
y = pulp.LpVariable.dicts('y', J, cat='Binary')       # Hiring variables

# Objective function
problem += pulp.lpSum(data['fixed_costs'][j] * y[j] for j in J) + \
           pulp.lpSum(data['additional_costs'][i][j] * x[i][j] for i in I for j in J)

# Constraints
# Assignment Constraint
for i in I:
    problem += pulp.lpSum(x[i][j] for j in J) == 1

# Hiring Constraint
for i in I:
    for j in J:
        problem += x[i][j] <= y[j]

# Capacity Constraint
for j in J:
    problem += pulp.lpSum(x[i][j] for i in I) <= data['max_projects_per_consultant'] * y[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')