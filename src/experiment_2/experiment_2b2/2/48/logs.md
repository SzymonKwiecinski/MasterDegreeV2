# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP or MILP

PROBLEM INFO:

- A fine foods company produces gift baskets for a season that lasts \var{W} weeks.
- The demand for week \var{w} is \var{demand_{w}} and the demand must be met.
- Regular labor is available for \var{regular_labor_{w}} hours per week and costs $\var{regular_cost}/h.
- Overtime labor is available for \var{overtime_labor_{w}} hours per week and costs $\var{overtime_cost}/h.
- Each basket takes \var{assembly_time} hours of labor to assemble.
- The material cost for each basket is $\var{material_cost} and it sells for $\var{selling_price}.
- Unsold baskets from a week incur a $\var{holding_cost} holding cost. 
- No baskets are available at the start of week 1.
- Unsold baskets at the end of week \var{W} have a salvage value of $var{salvage_value} and do not incur a holding cost.

INPUT FORMAT: 

{
    "regular_cost": regular_cost,
    "overtime_cost": overtime_cost,
    "assembly_time": assembly_time,
    "material_cost": material_cost,
    "selling_price": selling_price,
    "holding_cost": holding_cost,
    "salvage_value": salvage_value,
    "demand": [demand_{w} for w in 1, ..., W],
    "regular_labor": [regular_labor_{w} for w in 1, ..., W],
    "overtime_labor": [overtime_labor_{w} for w in 1, ..., W]
}

OBJECTIVE: How much regular and overtime labor should be utilized each week to assemble the baskets to maximize the profit over the season?

OUTPUT INFO:

- the hours of regular labor used each week \var{regular_used_{w}}.
- the hours of overtime labor used each week \var{overtime_used_{w}}.
- the number of baskets assembled with regular labor \var{regular_basket_{w}}.
- the number of baskets assembled with overtime labor \var{overtime_basket_{w}}.
- the number of baskets on hand at the end of week \var{inventory_{w}}.
- \var{total_profit} shows the total profit of the company for the season.

OUTPUT FORMAT:

{
    "regular_used": [regular_used_{w} for w in 1, ..., W],
    "overtime_used": [overtime_used_{w} for w in 1, ..., W],
    "regular_baskets": [regular_basket_{w} for w in 1, ..., W],
    "overtime_baskets": [overtime_basket_{w} for w in 1, ..., W],
    "inventory": [inventory_{w} for w in 1, ..., W],
    "total_profit": total_profit
}
</DESCRIPTION>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Define the input data
data = {
    'regular_cost': 30, 
    'overtime_cost': 45,
    'assembly_time': 0.4, 
    'material_cost': 25, 
    'selling_price': 65, 
    'holding_cost': 4, 
    'salvage_value': 30, 
    'demand': [700, 1500, 2800, 1800], 
    'regular_labor': [450, 550, 600, 600], 
    'overtime_labor': [40, 200, 320, 160]
}

#### Extract data
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
weeks = len(demand)

#### Create a LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', 0, regular_labor[w], cat='Continuous') for w in range(weeks)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', 0, overtime_labor[w], cat='Continuous') for w in range(weeks)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', 0, cat='Continuous') for w in range(weeks)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', 0, cat='Continuous') for w in range(weeks)]
inventory = [pulp.LpVariable(f'inventory_{w}', 0, cat='Continuous') for w in range(weeks)]

#### Constraints
for w in range(weeks):
    problem += regular_used[w] == regular_basket[w] * assembly_time, f'Regular_Labor_Constraint_{w}'
    problem += overtime_used[w] == overtime_basket[w] * assembly_time, f'Overtime_Labor_Constraint_{w}'
    problem += regular_basket[w] + overtime_basket[w] + (inventory[w-1] if w > 0 else 0) == demand[w] + inventory[w], f'Demand_Constraint_{w}'

#### Objective Function
total_revenue = pulp.lpSum((regular_basket[w] + overtime_basket[w]) * selling_price for w in range(weeks))
total_material_cost = pulp.lpSum((regular_basket[w] + overtime_basket[w]) * material_cost for w in range(weeks))
total_regular_cost = pulp.lpSum(regular_used[w] * regular_cost for w in range(weeks))
total_overtime_cost = pulp.lpSum(overtime_used[w] * overtime_cost for w in range(weeks))
total_holding_cost = pulp.lpSum(inventory[w] * holding_cost for w in range(weeks - 1))
total_salvage_value = inventory[weeks - 1] * salvage_value

total_profit = total_revenue - total_material_cost - total_regular_cost - total_overtime_cost - total_holding_cost + total_salvage_value

problem += total_profit

#### Solve the problem
problem.solve()

#### Prepare the output
output = {
    "regular_used": [pulp.value(regular_used[w]) for w in range(weeks)],
    "overtime_used": [pulp.value(overtime_used[w]) for w in range(weeks)],
    "regular_baskets": [pulp.value(regular_basket[w]) for w in range(weeks)],
    "overtime_baskets": [pulp.value(overtime_basket[w]) for w in range(weeks)],
    "inventory": [pulp.value(inventory[w]) for w in range(weeks)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

