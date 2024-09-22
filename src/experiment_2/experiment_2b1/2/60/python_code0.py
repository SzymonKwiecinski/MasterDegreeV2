import json
import pulp

# Input data
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], 
                             [10, 8, 12], 
                             [15, 8, 20], 
                             [10, 6, 15], 
                             [8, 10, 15]], 
        'max_projects_per_consultant': 3}

# Extract data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)       # number of consultants

# Create a linear programming problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("assignment", 
                            ((i, j) for i in range(I) for j in range(J)), 
                            cat='Binary')

y = pulp.LpVariable.dicts("hire", range(J), cat='Binary')

# Objective function
problem += (pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + 
             pulp.lpSum(additional_costs[i][j] * x[i, j] for i in range(I) for j in range(J))), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += (pulp.lpSum(x[i, j] for j in range(J)) == 1, f"Assign_Project_{i}")

# A consultant can only be assigned to a maximum of K projects
for j in range(J):
    problem += (pulp.lpSum(x[i, j] for i in range(I)) <= max_projects * y[j], f"Max_Projects_Consultant_{j}")

# Solve the problem
problem.solve()

# Output results
assignments = [[int(x[i, j].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')