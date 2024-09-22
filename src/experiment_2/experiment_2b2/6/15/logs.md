# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO: 
- A company produces \var{N} kinds of products. 
- A product of the \var{i}-th type requires \var{assemblyHour_i} hours of assembly labor, \var{testingHour_i} hours of testing, and \var{materialCost_i} worth of raw materials (in $).
- Given the current personnel of the company, there can be at most \var{maxAssembly} hours of assembly labor and \var{maxTesting} hours of testing, each day.
- Product of the \var{i}-th type has a price of \var{price_i} dollars.
- The company can schedule up tp \var{maxOvertimeAssembly} hours of overtime assembly labor can be sched­uled, at a cost of \var{overtimeAssemblyCost} per hour.
- Suppose that the raw material supplier provides a \var{materialDiscount}% discount if the daily bill is above \var{discountThreshold} dollars (\var{materialDiscount} is a number between 0 and 100).

INPUT FORMAT: 

{
    "assemblyHour": [assemblyHour_i for i in 1, ..., N]
    "testingHour": [testingHour_i for i in 1, ..., N],
    "materialCost": [materialCost_i for i in 1, ..., N],
    "maxAssembly": maxAssembly
    "maxTesting": maxTesting,
    "price": [price_i for i in 1, ..., N],
    "maxOvertimeAssembly": maxOvertimeAssembly,
    "overtimeAssemblyCost": overtimeAssemblyCost,
    "materialDiscount": materialDiscount,
    "discountThreshold": discountThreshold
}

OBJECTIVE: We want to maximize the daily profit of the company, which is the total revenue minus the total cost.

OUTPUT INFO: 

- \var{dailyProfit} shows the daily profit of the company 
- \var{unitsProduced_i} shows the number of units of the \var{i}-th product produced
- \var{overtimeAssembly} shows the number of hours of overtime assembly labor scheduled
- \var{materialBought} shows the amount of raw materials bought

OUTPUT FORMAT:

{
    "dailyProfit": dailyProfit,
    "unitsProduced": [unitsProduced_i for i in 1, ..., N],
    "overtimeAssembly": overtimeAssembly,
    "materialBought": materialBought
}
</DESCRIPTION>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

#### Extracting variables from data
N = data['N']
assembly_hour = data['AssemblyHour']
testing_hour = data['TestingHour']
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
price = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

#### Define the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Variables
units_produced = [pulp.LpVariable(f"Units_Produced_{i}", lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable("Overtime_Assembly", lowBound=0, cat='Continuous')

#### Objective Function
revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])
material_bought = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])
material_cost_total = material_bought * ((100 - material_discount) / 100 if material_bought > discount_threshold else 1)
overtime_cost = overtime_assembly * overtime_assembly_cost
total_profit = revenue - material_cost_total - overtime_cost
problem += total_profit

#### Constraints
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) <= max_assembly + overtime_assembly, "Assembly_Labor_Limit"
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing, "Testing_Labor_Limit"
problem += overtime_assembly <= max_overtime_assembly, "Overtime_Limit"

#### Solve the problem
problem.solve()

#### Output results
daily_profit = pulp.value(total_profit)
units_produced_vals = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_val = pulp.value(overtime_assembly)
material_bought_val = pulp.value(material_bought)

output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_vals,
    "overtimeAssembly": overtime_assembly_val,
    "materialBought": material_bought_val
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO: 
- A company produces \var{N} kinds of products. 
- A product of the \var{i}-th type requires \var{assemblyHour_i} hours of assembly labor, \var{testingHour_i} hours of testing, and \var{materialCost_i} worth of raw materials (in $).
- Given the current personnel of the company, there can be at most \var{maxAssembly} hours of assembly labor and \var{maxTesting} hours of testing, each day.
- Product of the \var{i}-th type has a price of \var{price_i} dollars.
- The company can schedule up tp \var{maxOvertimeAssembly} hours of overtime assembly labor can be sched­uled, at a cost of \var{overtimeAssemblyCost} per hour.
- Suppose that the raw material supplier provides a \var{materialDiscount}% discount if the daily bill is above \var{discountThreshold} dollars (\var{materialDiscount} is a number between 0 and 100).

INPUT FORMAT: 

{
    "assemblyHour": [assemblyHour_i for i in 1, ..., N]
    "testingHour": [testingHour_i for i in 1, ..., N],
    "materialCost": [materialCost_i for i in 1, ..., N],
    "maxAssembly": maxAssembly
    "maxTesting": maxTesting,
    "price": [price_i for i in 1, ..., N],
    "maxOvertimeAssembly": maxOvertimeAssembly,
    "overtimeAssemblyCost": overtimeAssemblyCost,
    "materialDiscount": materialDiscount,
    "discountThreshold": discountThreshold
}

OBJECTIVE: We want to maximize the daily profit of the company, which is the total revenue minus the total cost.

OUTPUT INFO: 

- \var{dailyProfit} shows the daily profit of the company 
- \var{unitsProduced_i} shows the number of units of the \var{i}-th product produced
- \var{overtimeAssembly} shows the number of hours of overtime assembly labor scheduled
- \var{materialBought} shows the amount of raw materials bought

OUTPUT FORMAT:

{
    "dailyProfit": dailyProfit,
    "unitsProduced": [unitsProduced_i for i in 1, ..., N],
    "overtimeAssembly": overtimeAssembly,
    "materialBought": materialBought
}
</DESCRIPTION>
<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

#### Extracting variables from data
N = data['N']
assembly_hour = data['AssemblyHour']
testing_hour = data['TestingHour']
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
price = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

#### Define the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Variables
units_produced = [pulp.LpVariable(f"Units_Produced_{i}", lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable("Overtime_Assembly", lowBound=0, cat='Continuous')

#### Objective Function
revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])
material_bought = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])
material_cost_total = material_bought * ((100 - material_discount) / 100 if material_bought > discount_threshold else 1)
overtime_cost = overtime_assembly * overtime_assembly_cost
total_profit = revenue - material_cost_total - overtime_cost
problem += total_profit

#### Constraints
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) <= max_assembly + overtime_assembly, "Assembly_Labor_Limit"
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing, "Testing_Labor_Limit"
problem += overtime_assembly <= max_overtime_assembly, "Overtime_Limit"

#### Solve the problem
problem.solve()

#### Output results
daily_profit = pulp.value(total_profit)
units_produced_vals = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_val = pulp.value(overtime_assembly)
material_bought_val = pulp.value(material_bought)

output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_vals,
    "overtimeAssembly": overtime_assembly_val,
    "materialBought": material_bought_val
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

## START MESSAGE 2 
### ROLE: Role.USER
Fix the code based on the error

## START MESSAGE 3 
### ROLE: Role.USER
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_2/experiment_2b2/6/15/python_code0.py", line 29, in <module>
    material_cost_total = material_bought * ((100 - material_discount) / 100 if material_bought > discount_threshold else 1)
                                                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '>' not supported between instances of 'LpAffineExpression' and 'int'
</CODE_ERROR>


## START MESSAGE 4 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

#### Extracting variables from data
N = data['N']
assembly_hour = data['AssemblyHour']
testing_hour = data['TestingHour']
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
price = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

#### Define the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Variables
units_produced = [pulp.LpVariable(f"Units_Produced_{i}", lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable("Overtime_Assembly", lowBound=0, cat='Continuous')
material_bought = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])

#### Objective Function
revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])

#### Conditional discount on materials
material_cost_total_if_above_threshold = material_bought * ((100 - material_discount) / 100)
material_cost_total_no_discount = material_bought

#### Adding a binary variable to apply discount
apply_discount = pulp.LpVariable("Apply_Discount", cat='Binary')
problem += material_bought <= discount_threshold + (1-apply_discount) * 1e6, "Discount_Threshold_Condition"
problem += material_bought >= discount_threshold - apply_discount * 1e6, "Discount_Threshold_Condition_Below"

#### Total material cost based on discount condition
material_cost_total = apply_discount * material_cost_total_if_above_threshold + (1 - apply_discount) * material_cost_total_no_discount

overtime_cost = overtime_assembly * overtime_assembly_cost
total_profit = revenue - material_cost_total - overtime_cost
problem += total_profit

#### Constraints
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) <= max_assembly + overtime_assembly, "Assembly_Labor_Limit"
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing, "Testing_Labor_Limit"
problem += overtime_assembly <= max_overtime_assembly, "Overtime_Limit"

#### Solve the problem
problem.solve()

#### Output results
daily_profit = pulp.value(total_profit)
units_produced_vals = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_val = pulp.value(overtime_assembly)
material_bought_val = pulp.value(material_bought)

output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_vals,
    "overtimeAssembly": overtime_assembly_val,
    "materialBought": material_bought_val
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

