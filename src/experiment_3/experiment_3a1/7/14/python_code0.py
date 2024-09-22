import pulp
import json

# Data input
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

# Model parameters
P = data['P']
h = data['Hour']
c = data['Cost']
p = data['Price']
r = data['InvestPercentage']
U = data['UpgradeHours']
U_c = data['UpgradeCost']
A = data['AvailableHours']
C = data['Cash']

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(P), lowBound=0, cat='Continuous')
u = pulp.LpVariable("Upgrade", cat='Binary')

# Objective function
problem += pulp.lpSum([p[i] * x[i] - c[i] * x[i] - r[i] * p[i] * x[i] for i in range(P)]) - U_c * u, "Total_Net_Income"

# Constraints
problem += pulp.lpSum([h[i] * x[i] for i in range(P)]) <= A + U * u, "Machine_Hours_Constraint"
problem += pulp.lpSum([c[i] * x[i] for i in range(P)]) + U_c * u <= C, "Cash_Availability_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')