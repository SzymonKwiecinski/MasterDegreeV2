import pulp
import json

# Data from the JSON
data = json.loads("{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}")
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

# Sets
I = range(len(additional_costs))  # projects
J = range(len(fixed_costs))        # consultants

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", J, cat='Binary')  # Consultant hired
y = pulp.LpVariable.dicts("y", (I, J), cat='Binary')  # Project assigned

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in J) + pulp.lpSum(additional_costs[i][j] * y[i][j] for i in I for j in J)

# Constraints
# Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(y[i][j] for j in J) == 1

# A consultant can be assigned at most K projects
for j in J:
    problem += pulp.lpSum(y[i][j] for i in I) <= K * x[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')