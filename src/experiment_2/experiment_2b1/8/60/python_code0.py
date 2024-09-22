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

# Extracting the data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)       # number of consultants

# Create the problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision variables
assignment = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')
consultant_hired = pulp.LpVariable.dicts("consultant_hired", range(J), cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * consultant_hired[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * assignment[j][i] for i in range(I) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(assignment[j][i] for j in range(J)) == 1  # Each project is assigned to exactly one consultant

for j in range(J):
    problem += pulp.lpSum(assignment[j][i] for i in range(I)) <= max_projects_per_consultant * consultant_hired[j]  # Projects assigned do not exceed maximum

# Solve the problem
problem.solve()

# Prepare the results
assignments = [[int(assignment[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')