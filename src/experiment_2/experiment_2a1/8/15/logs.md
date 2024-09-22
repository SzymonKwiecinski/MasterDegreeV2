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
import json

#### Input data in JSON format
data = {'N': 2, 
        'AssemblyHour': [0.25, 0.3333], 
        'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 
        'MaxTesting': 70, 
        'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 
        'DiscountThreshold': 300}

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

#### Variables
N = data['N']
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

#### Costs and revenues
materialCost = data['MaterialCost']
price = data['Price']
assemblyHour = data['AssemblyHour']
testingHour = data['TestingHour']

#### Constraints
problem += pulp.lpSum([assemblyHour[i] * unitsProduced[i] for i in range(N)]) + overtimeAssembly <= data['MaxAssembly'], "MaxAssemblyConstraint"
problem += pulp.lpSum([testingHour[i] * unitsProduced[i] for i in range(N)]) <= data['MaxTesting'], "MaxTestingConstraint"

#### Objective Function
totalRevenue = pulp.lpSum([price[i] * unitsProduced[i] for i in range(N)])
totalMaterialCost = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)])
totalCost = totalMaterialCost + overtimeAssembly * data['OvertimeAssemblyCost']

#### Calculate discount if applicable
totalCostWithDiscount = totalCost
if totalMaterialCost > data['DiscountThreshold']:
    totalCostWithDiscount *= (1 - (data['MaterialDiscount'] / 100))

#### Profit function
dailyProfit = totalRevenue - totalCostWithDiscount
problem += dailyProfit, "Objective"

#### Solve the problem
problem.solve()

#### Output results
unitsProduced_solution = [pulp.value(unitsProduced[i]) for i in range(N)]
overtimeAssembly_solution = pulp.value(overtimeAssembly)
materialBought = sum(pulp.value(unitsProduced[i]) * materialCost[i] for i in range(N))

#### Print the results
print(json.dumps({
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": unitsProduced_solution,
    "overtimeAssembly": overtimeAssembly_solution,
    "materialBought": materialBought
}))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

