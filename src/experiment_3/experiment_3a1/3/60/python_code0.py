import pulp
import json

# Input data
data = json.loads("{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}")

# Define the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Data extraction
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']
f = data['fixed_costs']             # Fixed costs
c = data['additional_costs']        # Additional costs

# Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  # Hiring decision
y = pulp.LpVariable.dicts("y", (range(I), range(J)), cat='Binary')  # Assignment decision

# Objective Function
problem += pulp.lpSum(f[j] * x[j] for j in range(J)) + \
           pulp.lpSum(c[i][j] * y[i][j] for i in range(I) for j in range(J))

# Constraints
# 1. Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1

# 2. A consultant can only be assigned a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j]

# Solve the problem
problem.solve()

# Output results
assignments = [[int(y[i][j].varValue) for j in range(J)] for i in range(I)]
total_cost = pulp.value(problem.objective)

print(f'Assignments: {assignments}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')