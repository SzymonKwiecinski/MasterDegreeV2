import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], 
                             [10, 8, 12], 
                             [15, 8, 20], 
                             [10, 6, 15], 
                             [8, 10, 15]], 
        'max_projects_per_consultant': 3}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Initialize the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(J), range(I)), cat='Binary')  # x[j][i] = 1 if project i is assigned to consultant j
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')               # y[j] = 1 if consultant j is hired

# Objective function: Minimize total cost
problem += (
    pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + 
    pulp.lpSum(additional_costs[i][j] * x[j][i] for j in range(J) for i in range(I))
)

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[j][i] for j in range(J)) == 1

# A consultant can handle at most K projects
for j in range(J):
    problem += pulp.lpSum(x[j][i] for i in range(I)) <= max_projects_per_consultant * y[j]

# Solve the problem
problem.solve()

# Prepare the assignments and total cost
assignments = [[int(x[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')