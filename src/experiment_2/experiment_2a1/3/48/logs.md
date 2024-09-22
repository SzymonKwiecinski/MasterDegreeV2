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
import json

#### Input data
data = {'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 
        'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 
        'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 
        'regular_labor': [450, 550, 600, 600], 
        'overtime_labor': [40, 200, 320, 160]}

#### Problem parameters
W = len(data['demand'])
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

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0, cat='Continuous')
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0, cat='Continuous')
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(W), lowBound=0, cat='Integer')
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0, cat='Integer')

#### Objective function
profit = (selling_price * (regular_basket[w] + overtime_basket[w]) - 
          (material_cost * (regular_basket[w] + overtime_basket[w]) +
           regular_cost * (regular_used[w] / assembly_time) +
           overtime_cost * (overtime_used[w] / assembly_time) +
           holding_cost * inventory[w] for w in range(W)))
          
problem += pulp.lpSum(profit), "Total_Profit"

#### Constraints
for w in range(W):
    #### Labor constraints
    problem += regular_used[w] <= regular_labor[w], f"RegularLaborLimit_week_{w}"
    problem += overtime_used[w] <= overtime_labor[w], f"OvertimeLaborLimit_week_{w}"
    problem += (regular_used[w] + overtime_used[w]) / assembly_time >= regular_basket[w] + overtime_basket[w], f"ProductionLimit_week_{w}"
    
    #### Demand and inventory constraints
    if w == 0:
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - demand[w], f"InventoryWeek_{w}"
    else:
        problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - demand[w], f"InventoryWeek_{w}"

#### Ensure that the inventory at the end of sales week with salvage value
problem += inventory[W-1] >= 0, "FinalInventoryNonNegativity"

#### Solve the problem
problem.solve()

#### Prepare output
output = {
    "regular_used": [regular_used[w].varValue for w in range(W)],
    "overtime_used": [overtime_used[w].varValue for w in range(W)],
    "regular_baskets": [regular_basket[w].varValue for w in range(W)],
    "overtime_baskets": [overtime_basket[w].varValue for w in range(W)],
    "inventory": [inventory[w].varValue for w in range(W)],
    "total_profit": pulp.value(problem.objective)
}

#### Print results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

