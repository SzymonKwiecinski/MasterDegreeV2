import pulp

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, num_shifts + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(shift_costs[s - 1] * x[s] for s in range(1, num_shifts + 1)), "Total_Cost"

# Constraints
for s in range(1, num_shifts):
    problem += x[s] + x[s + 1] >= officers_needed[s - 1], f"Officers_Required_Shift_{s}"

problem += x[num_shifts] >= officers_needed[num_shifts - 1], "Officers_Required_Last_Shift"

# Solve the problem
problem.solve()

# Output results
officers_assigned = [x[s].varValue for s in range(1, num_shifts + 1)]
total_cost = pulp.value(problem.objective)
print(f'Officers Assigned: {officers_assigned}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')