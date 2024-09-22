import pulp
import json

# Data from the provided JSON format
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, S + 1), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(shift_costs[s - 1] * x[s] for s in range(1, S + 1)), "Total_Cost"

# Constraints
# Requirement for each shift
for s in range(1, S + 1):
    problem += x[s] >= officers_needed[s - 1], f"OfficersNeeded_shift_{s}"

# Coverage for consecutive shifts
for s in range(2, S + 1):
    problem += x[s] + x[s - 1] >= officers_needed[s - 1], f"Coverage_shift_{s}"

# Solve the problem
problem.solve()

# Output
officers_assigned = [x[s].varValue for s in range(1, S + 1)]
total_cost = pulp.value(problem.objective)

print(f'Officers Assigned: {officers_assigned}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')