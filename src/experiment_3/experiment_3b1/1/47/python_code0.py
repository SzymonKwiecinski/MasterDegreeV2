import pulp

# Data input
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Problem definition
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(1, num_shifts + 1), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("shift_active", range(1, num_shifts + 1), cat='Binary')

# Objective function
problem += pulp.lpSum(shift_costs[s - 1] * x[s] for s in range(1, num_shifts + 1)), "Total_Cost"

# Constraints
for s in range(2, num_shifts + 1):
    problem += (officers_assigned[s] + officers_assigned[s - 1] >= officers_needed[s - 1]), f"Officer_Needed_Constraint_{s}"

# Enforcing the relationship between officers assigned and whether the shift is active
for s in range(1, num_shifts + 1):
    problem += (officers_assigned[s] >= 0), f"Non_Negativity_Constraint_{s}"
    problem += (officers_assigned[s] <= (num_shifts * 2) * x[s]), f"Active_Shift_Constraint_{s}"

# Solve the problem
problem.solve()

# Output results
assigned_officers = {s: pulp.value(officers_assigned[s]) for s in range(1, num_shifts + 1)}
total_cost = pulp.value(problem.objective)

print(f'Assigned Officers: {assigned_officers}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')