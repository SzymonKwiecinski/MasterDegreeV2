import pulp
import json

# Data input
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Model setup
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(1, data['NumShifts'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['ShiftCosts'][s-1] * (officers_assigned[s] + (officers_assigned[s+1] if s < data['NumShifts'] else 0)) / 2 
              for s in range(1, data['NumShifts'] + 1)), "Total_Cost"

# Constraints
problem += (officers_assigned[1] >= data['OfficersNeeded'][0]), "Constraint_1"
for s in range(2, data['NumShifts'] + 1):
    problem += (officers_assigned[s] + officers_assigned[s-1] >= data['OfficersNeeded'][s-1]), f"Constraint_{s}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')