import pulp
import json

# Data input
data = json.loads("{'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}")
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create LP problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0) for s in range(num_shifts)]

# Objective function
problem += pulp.lpSum(shift_costs[s] * officers_assigned[s] for s in range(num_shifts)), "Total_Cost"

# Constraints
for s in range(num_shifts):
    # officers_assigned_s >= officers_needed_s
    problem += officers_assigned[s] >= officers_needed[s], f"Officers_Needed_{s+1}"

for s in range(num_shifts - 1):
    # officers_assigned_s = officers_assigned_{s+1}
    problem += officers_assigned[s] == officers_assigned[s + 1], f"Officers_Assigned_{s+1}"

# Solve the problem
problem.solve()

# Output results
assigned_officers = [pulp.value(officers_assigned[s]) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Printing results
print(f'Assigned Officers: {assigned_officers}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')