import pulp
import json

# Data
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

# Parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)  # Production variables
u = pulp.LpVariable("u", cat="Binary")  # Upgrade decision variable

# Objective function
problem += pulp.lpSum([(price[i] - cost[i] - investPercentage[i] * price[i]) * x[i] for i in range(P)]) - upgradeCost * u, "Total_Net_Income"

# Constraints
# Cash Constraint
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash + pulp.lpSum([investPercentage[i] * price[i] * x[i] for i in range(P)]), "Cash_Constraint"

# Machine Capacity Constraint
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= availableHours + upgradeHours * u, "Machine_Capacity_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')