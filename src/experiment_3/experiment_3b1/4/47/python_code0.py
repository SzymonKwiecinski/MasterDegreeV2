import pulp
import json

# Load data
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Parameters
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("Police_Officer_Shifts", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, num_shifts + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(shift_costs[s - 1] * x[s] for s in range(1, num_shifts + 1)), "Total_Cost"

# Constraints
problem += x[1] >= officers_needed[0], "First_Shift_Constraint"
for s in range(2, num_shifts + 1):
    problem += x[s] + x[s - 1] >= officers_needed[s - 1], f"Shift_{s}_Constraint"

# Solve the problem
problem.solve()

# Output results
officers_assigned = {s: x[s].varValue for s in range(1, num_shifts + 1)}
total_cost = pulp.value(problem.objective)

print(f'Officers Assigned: {officers_assigned}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')