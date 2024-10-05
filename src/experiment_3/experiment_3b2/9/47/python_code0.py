import pulp
import json

# Data
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Problem definition
problem = pulp.LpProblem("Minimize_Shift_Costs", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(num_shifts), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(num_shifts)), "Total_Cost"

# Constraints
for s in range(num_shifts):
    if s == 0:
        problem += x[s] >= officers_needed[s], f"Officers_Needed_{s+1}"
    else:
        problem += x[s] + x[s-1] >= officers_needed[s], f"Officers_Needed_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')