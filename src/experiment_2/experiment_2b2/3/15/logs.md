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

#### Parse the input data
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

#### Define the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Decision variables
units_produced = [pulp.LpVariable(f"unitsProduced_{i}", lowBound=0, cat='Integer') for i in range(data['N'])]
overtime_assembly = pulp.LpVariable("overtimeAssembly", lowBound=0, cat='Continuous')

#### Constraints
#### Assembly time constraint
problem += pulp.lpSum([units_produced[i] * data['AssemblyHour'][i] for i in range(data['N'])]) <= data['MaxAssembly'] + overtime_assembly

#### Testing time constraint
problem += pulp.lpSum([units_produced[i] * data['TestingHour'][i] for i in range(data['N'])]) <= data['MaxTesting']

#### Overtime assembly constraint
problem += overtime_assembly <= data['MaxOvertimeAssembly']

#### Objective function
#### Revenue
revenue = pulp.lpSum([units_produced[i] * data['Price'][i] for i in range(data['N'])])

#### Material cost
material_cost = pulp.lpSum([units_produced[i] * data['MaterialCost'][i] for i in range(data['N'])])

#### Apply material discount if applicable
material_cost_after_discount = pulp.LpVariable("materialCostAfterDiscount", lowBound=0, cat='Continuous')
problem += material_cost_after_discount == material_cost * (1 - data['MaterialDiscount'] / 100), "MaterialCostAfterDiscount"
problem += material_cost_after_discount >= data['DiscountThreshold'], "DiscountThreshold"

#### Overtime cost
overtime_cost = overtime_assembly * data['OvertimeAssemblyCost']

#### Total cost
total_cost = material_cost - material_cost_after_discount + overtime_cost

#### Profit
daily_profit = revenue - total_cost

#### Set the objective
problem += daily_profit

#### Solve the problem
problem.solve()

#### Output results
output = {
    "dailyProfit": pulp.value(daily_profit),
    "unitsProduced": [pulp.value(units_produced[i]) for i in range(data['N'])],
    "overtimeAssembly": pulp.value(overtime_assembly),
    "materialBought": pulp.value(material_cost)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


