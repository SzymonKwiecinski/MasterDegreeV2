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
shift_cost = data['ShiftCosts']

# Problem
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = pulp.LpVariable.dicts(
    "Officers_Assigned",
    range(S),
    lowBound=0,
    cat='Integer'
)

# Objective Function
problem += pulp.lpSum([
    shift_cost[s] * math.ceil(officers_needed[s] / 2) for s in range(S)
])

# Constraints
for s in range(S):
    problem += officers_assigned[s] >= officers_needed[s], f"MinOfficersNeededShift{s}"

for s in range(S-1):
    problem += officers_assigned[s] == officers_assigned[s-1] + officers_assigned[s+1], f"BalanceShift{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')