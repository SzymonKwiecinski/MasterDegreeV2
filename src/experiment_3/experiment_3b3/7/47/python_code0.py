import pulp

# Data provided
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Create a Linear Programming Problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(data['NumShifts'])]

# Objective Function
problem += pulp.lpSum([data['ShiftCosts'][s] * officers_assigned[s] for s in range(data['NumShifts'])]), "Total Cost"

# Constraints
# Officers assigned should be at least the officers needed for each shift
for s in range(data['NumShifts']):
    problem += officers_assigned[s] >= data['OfficersNeeded'][s], f"MinOfficersNeeded_Shift_{s}"

# Additional constraint to chain the number of officers assigned from previous shift
for s in range(1, data['NumShifts']):
    problem += officers_assigned[s] == officers_assigned[s-1] + officers_assigned[s], f"Chain_Assignment_Shift_{s}"

# Solve the problem
problem.solve()

# Print results
assigned_values = [int(pulp.value(officers_assigned[s])) for s in range(data['NumShifts'])]
total_cost = pulp.value(problem.objective)

print("Assigned Officers per Shift:", assigned_values)
print(f'Total Cost: ${total_cost}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')