import pulp
import json

# Data
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 
        'UpgradeCost': 400, 'AvailableHours': 2000}

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

# Problem Definition
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')
upgrade = pulp.LpVariable("upgrade", cat='Binary')

# Objective Function
net_income = pulp.lpSum((price[i] - cost[i] - investPercentage[i] * price[i]) * x[i] for i in range(P))
                        - upgradeCost * upgrade
problem += net_income

# Constraints
# Cash Constraint
problem += (pulp.lpSum(cost[i] * x[i] for i in range(P)) <= 
             cash - pulp.lpSum(investPercentage[i] * price[i] * x[i] for i in range(P)) * upgrade)

# Machine Hours Constraint
problem += (pulp.lpSum(hour[i] * x[i] for i in range(P)) <= 
             availableHours + upgradeHours * upgrade)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')