import pulp

# Data
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

# Indices
I = len(additional_costs)  # Number of projects
J = len(fixed_costs)  # Number of consultants

# Problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Hire", range(J), cat='Binary')
y = pulp.LpVariable.dicts("Assign", (range(I), range(J)), cat='Binary')

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) +\
           pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1

# A consultant can be assigned to a project only if they are hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j]

# A consultant can be assigned a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j]

# Solve the problem
problem.solve()

# Output
assignments = {(i, j): y[i][j].varValue for i in range(I) for j in range(J) if y[i][j].varValue == 1}
total_cost = pulp.value(problem.objective)

print("Assignments:", assignments)
print(f'(Objective Value): <OBJ>{total_cost}</OBJ>')