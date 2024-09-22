import json
import pulp

# Load data from JSON format
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Define the problem
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Decision Variables
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(S), lowBound=0, cat='Continuous')
shift_started = pulp.LpVariable.dicts("shift_started", range(S), cat='Binary')

# Objective Function
problem += pulp.lpSum(shift_costs[s] * shift_started[s] for s in range(S)), "Total_Cost"

# Constraints
for s in range(S - 1):
    problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Consecutive_Officer_Requirement_{s}"

for s in range(S):
    problem += officers_assigned[s] >= officers_needed[s] * shift_started[s], f"Officers_Assigned_Requirement_{s}"

# Solve the problem
problem.solve()

# Output results
officers_assigned_result = [officers_assigned[s].varValue for s in range(S)]
total_cost = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
print("Officers assigned to each shift: ", officers_assigned_result)