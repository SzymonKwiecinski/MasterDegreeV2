import pulp
import json

# Load the input data
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 
        'max_projects_per_consultant': 3}

# Extracting information from the data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

# Define the indices for projects and consultants
I = len(additional_costs)  # number of projects
J = len(fixed_costs)       # number of consultants

# Create the LP problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')  # x[j][i] = 1 if project i is assigned to consultant j
y = pulp.LpVariable.dicts("hire", range(J), cat='Binary')  # y[j] = 1 if consultant j is hired

# Objective function
problem += (pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + 
             pulp.lpSum(additional_costs[i][j] * x[j][i] for i in range(I) for j in range(J))), "Total_Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[j][i] for j in range(J)) == 1, f"Project_Assignment_{i}"

# A consultant can be assigned a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(x[j][i] for i in range(I)) <= max_projects_per_consultant * y[j], f"Max_Projects_Consultant_{j}"

# Solve the problem
problem.solve()

# Prepare the output
assignments = [[int(x[j][i].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')