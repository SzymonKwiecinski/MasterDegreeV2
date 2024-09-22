import pulp
import json

# Data
data = {'NumShifts': 6, 
        'OfficersNeeded': [15, 13, 11, 11, 9, 7], 
        'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Extracting the parameters from the data
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Officers_Assigned", range(1, S + 1), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(shift_costs[s - 1] * x[s] for s in range(1, S + 1))

# Constraints
for s in range(1, S + 1):
    problem += x[s] >= officers_needed[s - 1], f"OfficersNeeded_{s}"

for s in range(1, S):
    problem += x[s] == x[s + 1], f"ConsecutiveShifts_{s}"

# First and last shift constraints
problem += x[1] >= officers_needed[0], "FirstShiftRequirement"
problem += x[S] >= officers_needed[S - 1], "LastShiftRequirement"

# Solve the problem
problem.solve()

# Output results
for s in range(1, S + 1):
    print(f"Officers assigned to shift {s}: {x[s].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')