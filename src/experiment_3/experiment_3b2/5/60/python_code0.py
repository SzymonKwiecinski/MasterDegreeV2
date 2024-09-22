import pulp
import json

# Data provided in JSON format
data = json.loads('{"fixed_costs": [100, 150, 135], "additional_costs": [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], "max_projects_per_consultant": 3}')

# Extract data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)       # number of consultants

# Create the problem
problem = pulp.LpProblem("ConsultantAssignmentProblem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J))

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1

# A consultant can only take up to K projects if hired
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j]

# A project can only be assigned to a hired consultant
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')