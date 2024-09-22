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

# Parameters
J = len(data['fixed_costs'])  # Number of consultants
I = len(data['additional_costs'])  # Number of projects
K = data['max_projects_per_consultant']

# Create the linear programming problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
assignment = pulp.LpVariable.dicts("assignment", 
                                     ((j, i) for j in range(J) for i in range(I)), 
                                     cat=pulp.LpBinary)

# Objective function
problem += (
    pulp.lpSum(data['fixed_costs'][j] * (pulp.lpSum(assignment[j, i] for i in range(I)) >= 1) for j in range(J)) + 
    pulp.lpSum(data['additional_costs'][i][j] * assignment[j, i] for j in range(J) for i in range(I))
)

# Constraints
for i in range(I):
    problem += pulp.lpSum(assignment[j, i] for j in range(J)) == 1, f"Project_{i}_assignment"

for j in range(J):
    problem += pulp.lpSum(assignment[j, i] for i in range(I)) <= K, f"Consultant_{j}_limit"

# Solve the problem
problem.solve()

# Prepare the output
assignments = [[assignment[j, i].varValue for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output the result
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')