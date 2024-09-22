import pulp

# Parse the data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the LP problem
problem = pulp.LpProblem("MinimizeCostForPoliceShifts", pulp.LpMinimize)

# Decision variables: Number of officers assigned to start each shift
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: Minimize the total cost
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(num_shifts)]), "Total_Cost"

# Constraints: Ensure enough officers are assigned for each period
for s in range(num_shifts):
    # Officers available for shift s are those assigned to start at s and (s-1) % num_shifts
    problem += officers_assigned[s] + officers_assigned[(s-1) % num_shifts] >= officers_needed[s], f"Shift_{s}_Requirement"

# Solve the problem
problem.solve()

# Prepare the result
officers_assigned_result = [pulp.value(officers_assigned[s]) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Print the results
result = {
    "officers_assigned": officers_assigned_result,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')