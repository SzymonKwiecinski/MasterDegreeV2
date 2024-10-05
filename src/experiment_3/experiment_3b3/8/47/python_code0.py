import pulp

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_cost = data['ShiftCosts']

# Problem
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(S), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("ShiftStart", range(S), cat='Binary')

# Objective Function
problem += pulp.lpSum([shift_cost[s] * x[s] for s in range(S)])

# Constraints
# Officers needed for each shift
for s in range(S):
    problem += officers_assigned[s] >= officers_needed[s]

# Each officer works for two consecutive shifts
for s in range(1, S):
    problem += officers_assigned[s] + officers_assigned[s - 1] >= officers_needed[s - 1]

# Solve the problem
problem.solve()

# Output the result
assigned_officers = [pulp.value(officers_assigned[s]) for s in range(S)]
total_cost = pulp.value(problem.objective)

print(f'Assigned Officers: {assigned_officers}')
print(f'Total Cost (Objective Value): <OBJ>{total_cost}</OBJ>')