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
import json
import pulp

#### Input data
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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

#### Total costs and revenues
totalRevenue = pulp.lpSum(unitsProduced[i] * data['Price'][i] for i in range(data['N']))
totalMaterialCost = pulp.lpSum(unitsProduced[i] * data['MaterialCost'][i] for i in range(data['N']))

#### Applying material discount
totalMaterialCostDiscounted = totalMaterialCost * (1 - data['MaterialDiscount'] / 100) if totalMaterialCost > data['DiscountThreshold'] else totalMaterialCost

totalAssemblyCost = pulp.lpSum(unitsProduced[i] * data['AssemblyHour'][i] for i in range(data['N'])) + overtimeAssembly * data['OvertimeAssemblyCost']

#### Objective function
problem += totalRevenue - (totalMaterialCostDiscounted + totalAssemblyCost), "Total_Profit"

#### Constraints
problem += pulp.lpSum(unitsProduced[i] * data['AssemblyHour'][i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'], "MaxAssemblyConstraint"
problem += pulp.lpSum(unitsProduced[i] * data['TestingHour'][i] for i in range(data['N'])) <= data['MaxTesting'], "MaxTestingConstraint"

#### Solve the problem
problem.solve()

#### Output results
dailyProfit = pulp.value(problem.objective)
unitsProducedResult = [pulp.value(unitsProduced[i]) for i in range(data['N'])]
overtimeAssemblyResult = pulp.value(overtimeAssembly)
materialBought = pulp.value(totalMaterialCostDiscounted)

print(f' (Objective Value): <OBJ>{dailyProfit}</OBJ>')
output = {
    "dailyProfit": dailyProfit,
    "unitsProduced": unitsProducedResult,
    "overtimeAssembly": overtimeAssemblyResult,
    "materialBought": materialBought
}
```

