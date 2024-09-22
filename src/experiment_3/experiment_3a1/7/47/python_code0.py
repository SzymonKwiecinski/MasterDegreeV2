import pulp

# Data from the provided JSON format
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Parameters extraction
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the optimization problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(1, S + 1), lowBound=0, cat='Continuous')
shift_started = pulp.LpVariable.dicts("ShiftStarted", range(1, S + 1), 0, 1, pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(shift_costs[s - 1] * shift_started[s] for s in range(1, S + 1)), "Total_Cost"

# Constraints
for s in range(1, S + 1):
    problem += officers_assigned[s] >= officers_needed[s - 1], f"OfficersNeeded_Constraint_{s}"
    
for s in range(2, S + 1):
    problem += officers_assigned[s] == officers_assigned[s - 1] + officers_assigned[s], f"OfficerAssignment_Constraint_{s}"

# Solve the problem
problem.solve()

# Prepare output
officers_assigned_values = [officers_assigned[s].varValue for s in range(1, S + 1)]
total_cost = pulp.value(problem.objective)

# Print results
print(f'Officers Assigned: {officers_assigned_values}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')