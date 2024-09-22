import pulp
import json

# Data provided
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], 
                             [10, 8, 12], 
                             [15, 8, 20], 
                             [10, 6, 15], 
                             [8, 10, 15]], 
        'max_projects_per_consultant': 3}

# Extracting data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', range(J), cat='Binary')  # Hiring decision for consultants
assignment = pulp.LpVariable.dicts('assignment', (range(J), range(I)), cat='Binary')  # Assignment decisions

# Objective Function
problem += (pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + 
            pulp.lpSum(additional_costs[i][j] * assignment[j][i] for i in range(I) for j in range(J))), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignment[j][i] for j in range(J)) == 1, f"Project_Assignment_{i}"

# A consultant can assign up to K projects
for j in range(J):
    problem += pulp.lpSum(assignment[j][i] for i in range(I)) <= K * x[j], f"Consultant_Capacity_{j}"

# Solve the problem
problem.solve()

# Output results
assignments = [[pulp.value(assignment[j][i]) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

print(f'Assignments: {assignments}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')