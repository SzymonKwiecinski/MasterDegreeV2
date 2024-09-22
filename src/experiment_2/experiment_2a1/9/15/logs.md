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

#### Input data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
units_produced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=max_overtime_assembly)

#### Objective Function
revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])
cost_of_materials = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])

#### Check if the total material cost exceeds the discount threshold to apply discount
total_material_cost = cost_of_materials * (1 - material_discount / 100) if cost_of_materials >= discount_threshold else cost_of_materials

cost_of_labor = pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) + overtime_assembly * overtime_assembly_cost

total_cost = total_material_cost + cost_of_labor
profit = revenue - total_cost

problem += profit

#### Constraints
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) + overtime_assembly <= max_assembly
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing

#### Solve the problem
problem.solve()

#### Output the results
daily_profit = pulp.value(problem.objective)
units_produced_result = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_result = pulp.value(overtime_assembly)
material_bought = sum(pulp.value(units_produced[i]) * material_cost[i] for i in range(N))

#### Print the objective value
print(f' (Objective Value): <OBJ>{daily_profit}</OBJ>')

#### Format the output as required
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_result,
    "overtimeAssembly": overtime_assembly_result,
    "materialBought": material_bought
}

#### Output the results
print(json.dumps(output))
```

