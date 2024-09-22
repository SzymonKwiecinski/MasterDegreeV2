import pulp
import json

# Data
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_cost = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("PoliceOfficerShiftAssignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(S), lowBound=0, cat='Integer')
shift_started = pulp.LpVariable.dicts("shift_started", range(S), cat='Binary')

# Objective Function
problem += pulp.lpSum([shift_cost[s] * shift_started[s] for s in range(S)])

# Constraints
# Constraint 1: Each police officer works for two consecutive shifts.
for s in range(S):
    problem += officers_assigned[s] >= officers_needed[s]

# Constraint 2: Each shift requires a sufficient number of officers for the consecutive shifts.
for s in range(S-1):
    problem += officers_assigned[s] + officers_assigned[s+1] >= officers_needed[s]

# Solve the problem
problem.solve()

# Output Results
assigned_officers = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost = pulp.value(problem.objective)

print(f'Assigned Officers: {assigned_officers}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')