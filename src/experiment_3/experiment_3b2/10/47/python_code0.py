import pulp
import json

# Data input
data_json = '{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}'
data = json.loads(data_json)

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("PoliceOfficerShiftAssignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(S), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(S)), "Total_Cost"

# Constraints
for s in range(S):
    if s == 0:
        problem += x[s] + x[S-1] >= officers_needed[s], f"OfficersNeeded_{s+1}"
    else:
        problem += x[s] + x[s-1] >= officers_needed[s], f"OfficersNeeded_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')