import pulp
import json

# Data from the provided JSON
data = {
    'N': 2,
    'AssemblyHour': [0.25, 0.3333],
    'TestingHour': [0.125, 0.3333],
    'MaterialCost': [1.2, 0.9],
    'MaxAssembly': 10,
    'MaxTesting': 70,
    'Price': [9, 8],
    'MaxOvertimeAssembly': 50,
    'OvertimeAssemblyCost': 5,
    'MaterialDiscount': 10,
    'DiscountThreshold': 300
}

# Define the linear programming problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0, cat='Continuous')

# Objective Function
material_cost_expression = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
total_price = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))

# Discount calculation
discount = pulp.lpVariable("discount", lowBound=0, cat='Continuous')

# The discount logic
problem += pulp.lpSum([material_cost_expression > data['DiscountThreshold'], discount == (data['MaterialDiscount'] / 100) * material_cost_expression])
problem += (discount == 0).if_(material_cost_expression <= data['DiscountThreshold'])

# Daily profit function formulation
daily_profit = total_price - (material_cost_expression - discount) - (overtimeAssembly * data['OvertimeAssemblyCost'])
problem += daily_profit, "Objective"

# Constraints
# Assembly labor constraint
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor")

# Testing labor constraint
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Labor")

# Solve the problem
problem.solve()

# Output the results
unitsProduced = [x[i].varValue for i in range(data['N'])]
overtime_hours = overtimeAssembly.varValue
material_bought = material_cost_expression.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("Units Produced:", unitsProduced)
print("Overtime Assembly Hours Scheduled:", overtime_hours)
print("Material Bought:", material_bought)