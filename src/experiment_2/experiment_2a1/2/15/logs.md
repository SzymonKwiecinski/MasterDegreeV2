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

data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

#### Extract data for easier access
N = data['N']
assembly_hours = data['AssemblyHour']
testing_hours = data['TestingHour']
material_costs = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
prices = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
units_produced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=max_overtime_assembly)

#### Objective function: Maximize daily profit
revenue = pulp.lpSum(prices[i] * units_produced[i] for i in range(N))
total_material_cost = pulp.lpSum(material_costs[i] * units_produced[i] for i in range(N))
effective_material_cost = total_material_cost * (1 - (material_discount / 100) * (total_material_cost > discount_threshold))

#### Total assembly and testing hours
total_assembly_hours = pulp.lpSum(assembly_hours[i] * units_produced[i] for i in range(N)) + overtime_assembly
total_testing_hours = pulp.lpSum(testing_hours[i] * units_produced[i] for i in range(N))

#### Constraints
problem += total_assembly_hours <= max_assembly + overtime_assembly
problem += total_testing_hours <= max_testing

#### Objective function
profit = revenue - (effective_material_cost + overtime_assembly * overtime_assembly_cost)
problem += profit, "Total_Profit"

#### Solve the problem
problem.solve()

#### Retrieve results
daily_profit = pulp.value(problem.objective)
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought = sum(material_costs[i] * units_produced_values[i] for i in range(N))

#### Output results
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

