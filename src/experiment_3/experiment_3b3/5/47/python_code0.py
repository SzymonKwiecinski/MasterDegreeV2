import pulp
import math

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the LP problem
problem = pulp.LpProblem("PoliceOfficerScheduling", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(S), lowBound=0, cat='Integer')

# Objective function
total_cost = pulp.lpSum([shift_costs[s] * math.ceil(officers_needed[s] / 2) for s in range(S)])
problem += total_cost

# Constraints
for s in range(S):
    if s == 0:
        problem += officers_assigned[s] >= officers_needed[s], f"Shift_{s}_Coverage"
    else:
        problem += officers_assigned[s] + officers_assigned[s-1] >= officers_needed[s], f"Shift_{s}_Coverage"

# Solve the problem
problem.solve()

# Print results
officers_assigned_values = [pulp.value(officers_assigned[s]) for s in range(S)]
total_cost_value = pulp.value(problem.objective)
print(f'Officers Assigned: {officers_assigned_values}')
print(f'Total Cost (Objective Value): <OBJ>{total_cost_value}</OBJ>')