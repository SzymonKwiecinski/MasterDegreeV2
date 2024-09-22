import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

# Problem parameters
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the optimization problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
assignment = pulp.LpVariable.dicts("assign", (range(J), range(I)), cat='Binary')
hired = pulp.LpVariable.dicts("hired", range(J), cat='Binary')

# Objective function: Minimize total cost
problem += pulp.lpSum(fixed_costs[j] * hired[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * assignment[j][i] for i in range(I) for j in range(J))

# Constraints

# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignment[j][i] for j in range(J)) == 1

# Each consultant can handle at most K projects they are hired for
for j in range(J):
    problem += pulp.lpSum(assignment[j][i] for i in range(I)) <= K * hired[j]

# Solve the problem
problem.solve()

# Prepare the results
assignments = [[int(assignment[j][i].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')