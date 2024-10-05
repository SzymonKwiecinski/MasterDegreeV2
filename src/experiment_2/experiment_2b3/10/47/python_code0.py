import pulp

# Data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Problem
problem = pulp.LpProblem("Officer_Scheduling", pulp.LpMinimize)

# Variables
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective Function
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(num_shifts)])

# Constraints
for s in range(num_shifts):
    problem += officers_assigned[s] + officers_assigned[(s + 1) % num_shifts] >= officers_needed[s]

# Solve
problem.solve()

# Output
officers_assigned_value = [pulp.value(officers_assigned[s]) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned_value,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')