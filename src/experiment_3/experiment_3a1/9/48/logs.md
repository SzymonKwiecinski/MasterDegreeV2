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

\section*{Mathematical Model for Gift Basket Production}

\subsection*{Parameters}
\begin{align*}
& W \quad \text{(Number of weeks)} \\
& demand_w \quad \text{(Demand for week } w \text{)} \\
& regular\_labor_w \quad \text{(Regular labor hours available in week } w \text{)} \\
& overtime\_labor_w \quad \text{(Overtime labor hours available in week } w \text{)} \\
& regular\_cost \quad \text{(Cost of regular labor per hour)} \\
& overtime\_cost \quad \text{(Cost of overtime labor per hour)} \\
& assembly\_time \quad \text{(Time required to assemble one basket)} \\
& material\_cost \quad \text{(Material cost per basket)} \\
& selling\_price \quad \text{(Selling price per basket)} \\
& holding\_cost \quad \text{(Holding cost per unsold basket)} \\
& salvage\_value \quad \text{(Salvage value of unsold baskets at the end of week } W \text{)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& regular\_used_w \quad \text{(Hours of regular labor used in week } w \text{)} \\
& overtime\_used_w \quad \text{(Hours of overtime labor used in week } w \text{)} \\
& regular\_basket_w \quad \text{(Number of baskets assembled with regular labor in week } w \text{)} \\
& overtime\_basket_w \quad \text{(Number of baskets assembled with overtime labor in week } w \text{)} \\
& inventory_w \quad \text{(Number of baskets on hand at the end of week } w \text{)} \\
& total\_profit \quad \text{(Total profit for the season)}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
\text{Maximize } Z = \sum_{w=1}^{W} \left( (selling\_price \cdot (regular\_basket_w + overtime\_basket_w)) - (regular\_cost \cdot regular\_used_w) - (overtime\_cost \cdot overtime\_used_w) - (material\_cost \cdot (regular\_basket_w + overtime\_basket_w)) - (holding\_cost \cdot inventory_w) \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
1. & \quad \text{Labor constraints:} \\
& regular\_used_w \leq regular\_labor_w \quad \forall w \\
& overtime\_used_w \leq overtime\_labor_w \quad \forall w \\
\\
2. & \quad \text{Baskets assembly constraints:} \\
& regular\_basket_w = \frac{regular\_used_w}{assembly\_time} \quad \forall w \\
& overtime\_basket_w = \frac{overtime\_used_w}{assembly\_time} \quad \forall w \\
\\
3. & \quad \text{Demand satisfaction:} \\
& regular\_basket_w + overtime\_basket_w + inventory_{w-1} \geq demand_w \quad \forall w \text{ (with } inventory_0 = 0\text{)} \\
\\
4. & \quad \text{Inventory balance:} \\
& inventory_w = (regular\_basket_w + overtime\_basket_w + inventory_{w-1}) - demand_w \quad \forall w \\
\\
5. & \quad \text{Final inventory constraint:} \\
& inventory_W \geq 0 \\
\\
6. & \quad \text{Salvage value for unsold baskets:} \\
& total\_profit = Z + salvage\_value \cdot inventory_W
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

\section*{Mathematical Model for Gift Basket Production}

\subsection*{Parameters}
\begin{align*}
& W \quad \text{(Number of weeks)} \\
& demand_w \quad \text{(Demand for week } w \text{)} \\
& regular\_labor_w \quad \text{(Regular labor hours available in week } w \text{)} \\
& overtime\_labor_w \quad \text{(Overtime labor hours available in week } w \text{)} \\
& regular\_cost \quad \text{(Cost of regular labor per hour)} \\
& overtime\_cost \quad \text{(Cost of overtime labor per hour)} \\
& assembly\_time \quad \text{(Time required to assemble one basket)} \\
& material\_cost \quad \text{(Material cost per basket)} \\
& selling\_price \quad \text{(Selling price per basket)} \\
& holding\_cost \quad \text{(Holding cost per unsold basket)} \\
& salvage\_value \quad \text{(Salvage value of unsold baskets at the end of week } W \text{)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& regular\_used_w \quad \text{(Hours of regular labor used in week } w \text{)} \\
& overtime\_used_w \quad \text{(Hours of overtime labor used in week } w \text{)} \\
& regular\_basket_w \quad \text{(Number of baskets assembled with regular labor in week } w \text{)} \\
& overtime\_basket_w \quad \text{(Number of baskets assembled with overtime labor in week } w \text{)} \\
& inventory_w \quad \text{(Number of baskets on hand at the end of week } w \text{)} \\
& total\_profit \quad \text{(Total profit for the season)}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
\text{Maximize } Z = \sum_{w=1}^{W} \left( (selling\_price \cdot (regular\_basket_w + overtime\_basket_w)) - (regular\_cost \cdot regular\_used_w) - (overtime\_cost \cdot overtime\_used_w) - (material\_cost \cdot (regular\_basket_w + overtime\_basket_w)) - (holding\_cost \cdot inventory_w) \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
1. & \quad \text{Labor constraints:} \\
& regular\_used_w \leq regular\_labor_w \quad \forall w \\
& overtime\_used_w \leq overtime\_labor_w \quad \forall w \\
\\
2. & \quad \text{Baskets assembly constraints:} \\
& regular\_basket_w = \frac{regular\_used_w}{assembly\_time} \quad \forall w \\
& overtime\_basket_w = \frac{overtime\_used_w}{assembly\_time} \quad \forall w \\
\\
3. & \quad \text{Demand satisfaction:} \\
& regular\_basket_w + overtime\_basket_w + inventory_{w-1} \geq demand_w \quad \forall w \text{ (with } inventory_0 = 0\text{)} \\
\\
4. & \quad \text{Inventory balance:} \\
& inventory_w = (regular\_basket_w + overtime\_basket_w + inventory_{w-1}) - demand_w \quad \forall w \\
\\
5. & \quad \text{Final inventory constraint:} \\
& inventory_W \geq 0 \\
\\
6. & \quad \text{Salvage value for unsold baskets:} \\
& total\_profit = Z + salvage\_value \cdot inventory_W
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data_json = """
{
    "regular_cost": 30,
    "overtime_cost": 45,
    "assembly_time": 0.4,
    "material_cost": 25,
    "selling_price": 65,
    "holding_cost": 4,
    "salvage_value": 30,
    "demand": [700, 1500, 2800, 1800],
    "regular_labor": [450, 550, 600, 600],
    "overtime_labor": [40, 200, 320, 160]
}
"""
data = json.loads(data_json)

#### Parameters
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

#### Decision Variables
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]
total_profit = pulp.LpVariable('total_profit', lowBound=0)

#### Objective Function
profit = pulp.lpSum([
    (selling_price * (regular_basket[w] + overtime_basket[w])) -
    (regular_cost * regular_used[w]) -
    (overtime_cost * overtime_used[w]) -
    (material_cost * (regular_basket[w] + overtime_basket[w])) -
    (holding_cost * inventory[w])
    for w in range(W)
])
problem += profit

#### Constraints
for w in range(W):
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]
    problem += regular_basket[w] == regular_used[w] / assembly_time
    problem += overtime_basket[w] == overtime_used[w] / assembly_time

    if w == 0:
        problem += regular_basket[w] + overtime_basket[w] >= demand[w]
    else:
        problem += (regular_basket[w] + overtime_basket[w] + inventory[w-1]) >= demand[w]

    problem += inventory[w] == (regular_basket[w] + overtime_basket[w] + (inventory[w-1] if w > 0 else 0)) - demand[w]

problem += inventory[W-1] >= 0
problem += total_profit == profit + salvage_value * inventory[W-1]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

