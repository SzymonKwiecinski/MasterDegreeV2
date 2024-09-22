import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

# Extract data from input
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Variables
assignments = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')
consultant_hired = pulp.LpVariable.dicts("consultant_hired", range(J), cat='Binary')

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * consultant_hired[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * assignments[j][i] for j in range(J) for i in range(I))

# Constraints

# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[j][i] for j in range(J)) == 1

# Each consultant can handle a maximum number of projects
for j in range(J):
    problem += pulp.lpSum(assignments[j][i] for i in range(I)) <= K * consultant_hired[j]

# Solve the problem
problem.solve()

# Extract results
assignment_results = [[int(assignments[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Prepare output
output = {
    "assignments": assignment_results,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')