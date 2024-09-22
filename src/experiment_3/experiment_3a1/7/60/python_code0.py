import pulp
import json

# Data from JSON input
data = json.loads("{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}")
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

# Sets
I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the problem
problem = pulp.LpProblem("ConsultantAssignmentProblem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', (range(I), range(J)), cat='Binary')  # x[i][j] = 1 if project i is assigned to consultant j
y = pulp.LpVariable.dicts('y', range(J), cat='Binary')              # y[j] = 1 if consultant j is hired

# Objective Function
problem += (pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) +
             pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J))), "Total_Cost"

# Constraints
# 1. Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"Project_Assignment_{i}"

# 2. A consultant can only take projects if they are hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Consultant_Hired_{i}_{j}"

# 3. A consultant can take at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j], f"Max_Projects_Consultant_{j}"

# Solve the problem
problem.solve()

# Output results
assignments = [[int(x[i][j].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')