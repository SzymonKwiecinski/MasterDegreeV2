import pulp

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Problem
problem = pulp.LpProblem("Minimize_Police_Shift_Cost", pulp.LpMinimize)

# Variables
# x[s] is the number of officers starting their shift at shift s
x = [pulp.LpVariable(f'x_{s}', lowBound=0, cat='Integer') for s in range(data['NumShifts'])]

# Objective Function
problem += pulp.lpSum([x[s] * data['ShiftCosts'][s] for s in range(data['NumShifts'])])

# Constraints
for s in range(data['NumShifts']):
    # Calculate the required officers for shift s
    officers_on_duty = x[s] + x[(s - 1) % data['NumShifts']]
    problem += officers_on_duty >= data['OfficersNeeded'][s], f"Shift_{s}_requirement"

# Solve the problem
problem.solve()

# Output
officers_assigned = [int(x[s].varValue) for s in range(data['NumShifts'])]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')