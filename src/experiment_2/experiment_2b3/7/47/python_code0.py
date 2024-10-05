import pulp

# Data input
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the Linear Programming Problem
problem = pulp.LpProblem("Minimize_Officer_Costs", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(num_shifts), lowBound=0, cat='Integer')

# Objective function: Minimize total cost
problem += pulp.lpSum([officers_assigned[i] * shift_costs[i] for i in range(num_shifts)])

# Constraints: Meet the required number of officers for each shift
for i in range(num_shifts):
    problem += officers_assigned[i] + officers_assigned[(i + 1) % num_shifts] >= officers_needed[i]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "officers_assigned": [pulp.value(officers_assigned[i]) for i in range(num_shifts)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')