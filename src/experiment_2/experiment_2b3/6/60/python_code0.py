import pulp

# Data provided
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

num_projects = len(additional_costs)
num_consultants = len(fixed_costs)

# Problem
problem = pulp.LpProblem("Minimize_Assignment_Costs", pulp.LpMinimize)

# Variables
assignments = pulp.LpVariable.dicts("Assignment", ((j, i) for j in range(num_consultants) for i in range(num_projects)), cat='Binary')
hire = pulp.LpVariable.dicts("Hire", (j for j in range(num_consultants)), cat='Binary')

# Objective Function
problem += pulp.lpSum([fixed_costs[j] * hire[j] for j in range(num_consultants)]) + \
    pulp.lpSum([additional_costs[i][j] * assignments[j, i] for j in range(num_consultants) for i in range(num_projects)])

# Constraints
for i in range(num_projects):
    problem += pulp.lpSum([assignments[j, i] for j in range(num_consultants)]) == 1, f"Project_{i}_Assignment"

for j in range(num_consultants):
    problem += pulp.lpSum([assignments[j, i] for i in range(num_projects)]) <= max_projects_per_consultant * hire[j], f"Consultant_{j}_Capacity"

# Solve the problem
problem.solve()

# Results
assignments_result = [[pulp.value(assignments[j, i]) for i in range(num_projects)] for j in range(num_consultants)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments_result,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')