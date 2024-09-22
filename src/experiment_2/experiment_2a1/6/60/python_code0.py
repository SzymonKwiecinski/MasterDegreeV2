import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 
        'max_projects_per_consultant': 3}

# Extracting parameters from the input data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)       # number of consultants

# Creating the optimization problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("assign", (range(J), range(I)), cat='Binary')  # Assignment variables
y = pulp.LpVariable.dicts("hire", range(J), cat='Binary')  # Hiring variables

# Objective function: minimize total cost
problem += (
    pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + 
    pulp.lpSum(additional_costs[i][j] * x[j][i] for i in range(I) for j in range(J))
)

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[j][i] for j in range(J)) == 1

# A consultant can only be assigned a project if they are hired
for i in range(I):
    for j in range(J):
        problem += x[j][i] <= y[j]

# A consultant cannot handle more than K projects
for j in range(J):
    problem += pulp.lpSum(x[j][i] for i in range(I)) <= K

# Solve the problem
problem.solve()

# Prepare output
assignments = [[int(x[j][i].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output formatting
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')