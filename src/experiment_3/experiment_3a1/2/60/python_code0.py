import pulp

# Data from the provided JSON
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

# Constants
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']

# Create the 'prob' variable to contain the problem data
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', range(J), cat='Binary')  # For consultants
y = pulp.LpVariable.dicts('y', (range(I), range(J)), cat='Binary')  # For project assignments

# Objective Function
problem += (
    pulp.lpSum(data['fixed_costs'][j] * x[j] for j in range(J)) +
    pulp.lpSum(data['additional_costs'][i][j] * y[i][j] for i in range(I) for j in range(J))
)

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += (pulp.lpSum(y[i][j] for j in range(J)) == 1)

# A consultant can take up to K projects
for j in range(J):
    problem += (pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j])

# The assignment variable must be linked to the hiring variable
for i in range(I):
    for j in range(J):
        problem += (y[i][j] <= x[j])

# Solve the problem
problem.solve()

# Print the results
assignments = {(j, i): pulp.value(y[i][j]) for i in range(I) for j in range(J) if pulp.value(y[i][j]) == 1}
total_cost = pulp.value(problem.objective)

print(f'Assignments: {assignments}')
print(f'Total cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')