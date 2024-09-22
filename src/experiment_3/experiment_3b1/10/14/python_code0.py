import pulp

# Data from the provided JSON
data = {
    'P': 2,
    'Cash': 3000,
    'Hour': [2, 6],
    'Cost': [3, 2],
    'Price': [6, 5],
    'InvestPercentage': [0.4, 0.3],
    'UpgradeHours': 2000,
    'UpgradeCost': 400,
    'AvailableHours': 2000
}

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['P']), lowBound=0)  # Production quantities
y = pulp.LpVariable("y", cat='Binary')  # Upgrade decision

# Objective Function
problem += pulp.lpSum((data['Price'][i] * x[i] - 
                        data['Cost'][i] * x[i] - 
                        data['InvestPercentage'][i] * data['Price'][i] * x[i]) 
                       for i in range(data['P'])) - y * data['UpgradeCost'], "Total_Net_Income"

# Constraints
# Cash availability constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) + y * data['UpgradeCost'] <= data['Cash'], "Cash_Constraint"

# Machine capacity constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + y * data['UpgradeHours'], "Machine_Capacity_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')