import pulp

# Data from the provided JSON input
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

# Extracting parameters
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']  # Max projects per consultant

# Costs
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  # Consultant hired
y = pulp.LpVariable.dicts("y", (range(I), range(J)), cat='Binary')  # Project assignment

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# 1. Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1, f"Assign_One_Consultant_Project_{i}"

# 2. A consultant can only be assigned projects if they are hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j], f"Consultant_Hired_Project_{i}_Consultant_{j}"

# 3. A consultant can be assigned up to K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j], f"Max_Projects_Consultant_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')