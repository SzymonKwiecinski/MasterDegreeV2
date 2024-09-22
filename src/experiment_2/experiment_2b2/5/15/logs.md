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

#### Problem data from JSON
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

#### Create the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Decision variables
units_produced = [pulp.LpVariable(f'Units_Produced_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtime_assembly = pulp.LpVariable('Overtime_Assembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

#### Objective function: Maximize revenue - cost
revenue = pulp.lpSum(data['Price'][i] * units_produced[i] for i in range(data['N']))
material_cost = pulp.lpSum(data['MaterialCost'][i] * units_produced[i] for i in range(data['N']))
assembly_cost = overtime_assembly * data['OvertimeAssemblyCost']

#### Apply material discount
discounted_material_cost = pulp.LpVariable('Discounted_Material_Cost', lowBound=0, cat='Continuous')
problem += discounted_material_cost == material_cost, "MaterialCostAdjustment"
problem += discounted_material_cost >= ((100 - data['MaterialDiscount']) / 100) * material_cost, "MaterialDiscountCondition"
problem += discounted_material_cost >= material_cost - pulp.lpSum([pulp.lpSum(data['MaterialCost'][i] * units_produced[i] for i in range(data['N'])) * data['MaterialDiscount'] / 100]), "DiscountThresholdCondition" 

#### Profit = Revenue - Costs
profit = revenue - discounted_material_cost - assembly_cost
problem += profit

#### Constraints
#### Assembly hours
problem += pulp.lpSum(data['AssemblyHour'][i] * units_produced[i] for i in range(data['N'])) <= data['MaxAssembly'] + overtime_assembly, "MaxAssembly"

#### Testing hours
problem += pulp.lpSum(data['TestingHour'][i] * units_produced[i] for i in range(data['N'])) <= data['MaxTesting'], "MaxTesting"

#### Solve the problem
problem.solve()

#### Collect results
units_produced_values = [pulp.value(units_produced[i]) for i in range(data['N'])]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought_value = material_cost.value()
daily_profit_value = pulp.value(profit)

#### Print the results
output = {
    "dailyProfit": daily_profit_value,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

