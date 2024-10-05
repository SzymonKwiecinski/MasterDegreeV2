import pulp

# Extract data
data = {
    'fixed_costs': [100, 150, 135], 
    'additional_costs': [
        [10, 12, 20], 
        [10, 8, 12], 
        [15, 8, 20], 
        [10, 6, 15], 
        [8, 10, 15]
    ], 
    'max_projects_per_consultant': 3
}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)
J = len(fixed_costs)

# Create a problem variable
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Define decision variables
assignment = pulp.LpVariable.dicts("assignment", ((j, i) for j in range(J) for i in range(I)), cat='Binary')
consultant_hired = pulp.LpVariable.dicts("consultant_hired", (j for j in range(J)), cat='Binary')

# Objective function: Minimize total cost
problem += pulp.lpSum(fixed_costs[j] * consultant_hired[j] + additional_costs[i][j] * assignment[(j, i)] 
                      for j in range(J) for i in range(I))

# Constraint: Each project i is assigned to exactly one consultant j
for i in range(I):
    problem += pulp.lpSum(assignment[(j, i)] for j in range(J)) == 1

# Constraint: Each consultant can be assigned up to K projects
for j in range(J):
    problem += pulp.lpSum(assignment[(j, i)] for i in range(I)) <= K * consultant_hired[j]

# Solve the problem
problem.solve()

# Prepare the output
assignments = [[int(assignment[(j, i)].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')