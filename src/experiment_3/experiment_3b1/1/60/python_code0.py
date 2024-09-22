import pulp

# Data from the provided JSON-like format
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Parameters
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']  # Max projects per consultant

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  # Consultant hired
a = pulp.LpVariable.dicts("a", (range(I), range(J)), cat='Binary')  # Project assignment

# Objective Function
problem += pulp.lpSum(data['fixed_costs'][j] * x[j] for j in range(J)) + \
           pulp.lpSum(data['additional_costs'][i][j] * a[i][j] for i in range(I) for j in range(J))

# Constraints

# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(a[i][j] for j in range(J)) == 1
    
# A consultant can only be assigned projects if they are hired
for i in range(I):
    for j in range(J):
        problem += a[i][j] <= x[j]
        
# A consultant can take on at most K projects
for j in range(J):
    problem += pulp.lpSum(a[i][j] for i in range(I)) <= K * x[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')