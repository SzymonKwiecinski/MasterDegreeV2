import pulp

# Data initialization from provided JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Define sets
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants

# Fixed costs and additional costs
f = data['fixed_costs']
c = data['additional_costs']
K = data['max_projects_per_consultant']

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), cat='Binary')  # Project assignment
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')              # Consultant hiring

# Objective function
problem += pulp.lpSum(f[j] * y[j] for j in range(J)) + pulp.lpSum(c[i][j] * x[i][j] for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"Assign_Project_{i}"

# A consultant can only work on a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j], f"Max_Projects_Consultant_{j}"

# A project can only be assigned to a consultant if that consultant is hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Project_Assignment_Consultant_{i}_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')