import pulp
import json

# Data
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(S), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(S)), "Total_Cost"

# Constraints
for s in range(S):
    problem += (x[s] + x[s-1] >= officers_needed[s]), f"Officers_Needed_Constraint_{s}"

# Circular constraint (x_0 = x_S)
problem += (x[0] == x[S-1]), "Circular_Constraint"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')