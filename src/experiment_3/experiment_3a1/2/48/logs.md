# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Gift Basket Production}
\author{}
\date{}
\maketitle

\section*{Problem Description}
A fine foods company produces gift baskets for a season that lasts $W$ weeks. The company needs to meet the demand for each week while managing labor costs and inventory.

\section*{Parameters}
\begin{align*}
& \text{Let } W = \text{number of weeks} \\
& \text{Let } demand_w = \text{demand for week } w, \quad w = 1, \ldots, W \\
& \text{Let } regular\_labor_w = \text{regular labor hours available for week } w \\
& \text{Let } overtime\_labor_w = \text{overtime labor hours available for week } w \\
& \text{Let } regular\_cost = \text{cost of regular labor per hour} \\
& \text{Let } overtime\_cost = \text{cost of overtime labor per hour} \\
& \text{Let } assembly\_time = \text{time to assemble one basket (hours)} \\
& \text{Let } material\_cost = \text{material cost for one basket} \\
& \text{Let } selling\_price = \text{selling price of one basket} \\
& \text{Let } holding\_cost = \text{holding cost per unsold basket} \\
& \text{Let } salvage\_value = \text{salvage value per unsold basket at week } W \\
\end{align*}

\section*{Decision Variables}
\begin{align*}
& regular\_used_w = \text{hours of regular labor used in week } w, \quad w = 1, \ldots, W \\
& overtime\_used_w = \text{hours of overtime labor used in week } w, \quad w = 1, \ldots, W \\
& regular\_basket_w = \text{number of baskets assembled with regular labor in week } w \\
& overtime\_basket_w = \text{number of baskets assembled with overtime labor in week } w \\
& inventory_w = \text{number of baskets on hand at the end of week } w \\
& total\_profit = \text{total profit over the season} \\
\end{align*}

\section*{Objective Function}
Maximize total profit:
\begin{align*}
\text{Maximize } Z = \sum_{w=1}^{W} \left( (selling\_price - material\_cost) \cdot (regular\_basket_w + overtime\_basket_w) - \left( regular\_used_w \cdot regular\_cost + overtime\_used_w \cdot overtime\_cost \right) - \sum_{w=1}^{W-1} holding\_cost \cdot inventory_w + salvage\_value \cdot inventory_W \right)
\end{align*}

\section*{Constraints}
1. Labor hours constraint:
\begin{align*}
regular\_used_w + overtime\_used_w & \leq regular\_labor_w + overtime\_labor_w, \quad w = 1, \ldots, W \\
\end{align*}

2. Baskets production constraint:
\begin{align*}
regular\_basket_w & = \frac{regular\_used_w}{assembly\_time}, \quad w = 1, \ldots, W \\
overtime\_basket_w & = \frac{overtime\_used_w}{assembly\_time}, \quad w = 1, \ldots, W \\
\end{align*}

3. Inventory balance constraint:
\begin{align*}
inventory_w & = inventory_{w-1} + regular\_basket_w + overtime\_basket_w - demand_w, \quad w = 2, \ldots, W \\
inventory_1 & = regular\_basket_1 + overtime\_basket_1 - demand_1 \\
inventory_W & \geq 0 \\
\end{align*}

4. Non-negativity constraints:
\begin{align*}
regular\_used_w, overtime\_used_w & \geq 0, \quad w = 1, \ldots, W \\
regular\_basket_w, overtime\_basket_w & \geq 0, \quad w = 1, \ldots, W \\
inventory_w & \geq 0, \quad w = 1, \ldots, W \\
\end{align*}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Gift Basket Production}
\author{}
\date{}
\maketitle

\section*{Problem Description}
A fine foods company produces gift baskets for a season that lasts $W$ weeks. The company needs to meet the demand for each week while managing labor costs and inventory.

\section*{Parameters}
\begin{align*}
& \text{Let } W = \text{number of weeks} \\
& \text{Let } demand_w = \text{demand for week } w, \quad w = 1, \ldots, W \\
& \text{Let } regular\_labor_w = \text{regular labor hours available for week } w \\
& \text{Let } overtime\_labor_w = \text{overtime labor hours available for week } w \\
& \text{Let } regular\_cost = \text{cost of regular labor per hour} \\
& \text{Let } overtime\_cost = \text{cost of overtime labor per hour} \\
& \text{Let } assembly\_time = \text{time to assemble one basket (hours)} \\
& \text{Let } material\_cost = \text{material cost for one basket} \\
& \text{Let } selling\_price = \text{selling price of one basket} \\
& \text{Let } holding\_cost = \text{holding cost per unsold basket} \\
& \text{Let } salvage\_value = \text{salvage value per unsold basket at week } W \\
\end{align*}

\section*{Decision Variables}
\begin{align*}
& regular\_used_w = \text{hours of regular labor used in week } w, \quad w = 1, \ldots, W \\
& overtime\_used_w = \text{hours of overtime labor used in week } w, \quad w = 1, \ldots, W \\
& regular\_basket_w = \text{number of baskets assembled with regular labor in week } w \\
& overtime\_basket_w = \text{number of baskets assembled with overtime labor in week } w \\
& inventory_w = \text{number of baskets on hand at the end of week } w \\
& total\_profit = \text{total profit over the season} \\
\end{align*}

\section*{Objective Function}
Maximize total profit:
\begin{align*}
\text{Maximize } Z = \sum_{w=1}^{W} \left( (selling\_price - material\_cost) \cdot (regular\_basket_w + overtime\_basket_w) - \left( regular\_used_w \cdot regular\_cost + overtime\_used_w \cdot overtime\_cost \right) - \sum_{w=1}^{W-1} holding\_cost \cdot inventory_w + salvage\_value \cdot inventory_W \right)
\end{align*}

\section*{Constraints}
1. Labor hours constraint:
\begin{align*}
regular\_used_w + overtime\_used_w & \leq regular\_labor_w + overtime\_labor_w, \quad w = 1, \ldots, W \\
\end{align*}

2. Baskets production constraint:
\begin{align*}
regular\_basket_w & = \frac{regular\_used_w}{assembly\_time}, \quad w = 1, \ldots, W \\
overtime\_basket_w & = \frac{overtime\_used_w}{assembly\_time}, \quad w = 1, \ldots, W \\
\end{align*}

3. Inventory balance constraint:
\begin{align*}
inventory_w & = inventory_{w-1} + regular\_basket_w + overtime\_basket_w - demand_w, \quad w = 2, \ldots, W \\
inventory_1 & = regular\_basket_1 + overtime\_basket_1 - demand_1 \\
inventory_W & \geq 0 \\
\end{align*}

4. Non-negativity constraints:
\begin{align*}
regular\_used_w, overtime\_used_w & \geq 0, \quad w = 1, \ldots, W \\
regular\_basket_w, overtime\_basket_w & \geq 0, \quad w = 1, \ldots, W \\
inventory_w & \geq 0, \quad w = 1, \ldots, W \\
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

#### Parameters
W = len(data['demand'])  #### number of weeks
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

#### Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(1, W + 1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(1, W + 1), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(1, W + 1), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(1, W + 1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(1, W + 1), lowBound=0)

#### Problem definition
problem = pulp.LpProblem("GiftBasketProduction", pulp.LpMaximize)

#### Objective Function
profit = pulp.lpSum((selling_price - material_cost) * (regular_basket[w] + overtime_basket[w]) for w in range(1, W + 1))
costs = pulp.lpSum(regular_used[w] * regular_cost + overtime_used[w] * overtime_cost for w in range(1, W + 1))
holding_costs = pulp.lpSum(holding_cost * inventory[w] for w in range(1, W)) - salvage_value * inventory[W]
problem += profit - costs - holding_costs, "Total_Profit"

#### Constraints
#### Labor hours constraint
for w in range(1, W + 1):
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w - 1] + overtime_labor[w - 1], f"LaborConstraint_{w}"

#### Baskets production constraint
for w in range(1, W + 1):
    problem += regular_basket[w] == regular_used[w] / assembly_time, f"RegularProductionConstraint_{w}"
    problem += overtime_basket[w] == overtime_used[w] / assembly_time, f"OvertimeProductionConstraint_{w}"

#### Inventory balance constraint
problem += inventory[1] == regular_basket[1] + overtime_basket[1] - demand[0], "InventoryBalance_Week1"
for w in range(2, W + 1):
    problem += inventory[w] == inventory[w - 1] + regular_basket[w] + overtime_basket[w] - demand[w - 1], f"InventoryBalance_Week_{w}"
problem += inventory[W] >= 0, "NonNegInventory_WeekW"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

