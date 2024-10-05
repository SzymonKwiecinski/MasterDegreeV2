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
The given problem can be modeled as a Linear Programming (LP) problem. We aim to maximize the total profit by determining how much regular and overtime labor should be used each week to assemble gift baskets. Below is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\textbf{Given:}
\begin{itemize}
    \item $W$: Number of weeks in the season.
    \item $\text{demand}_{w}$: Demand for baskets in week $w$.
    \item $\text{regular\_labor}_{w}$: Maximum regular labor hours available in week $w$.
    \item $\text{regular\_cost}$: Cost per hour for regular labor.
    \item $\text{overtime\_labor}_{w}$: Maximum overtime labor hours available in week $w$.
    \item $\text{overtime\_cost}$: Cost per hour for overtime labor.
    \item $\text{assembly\_time}$: Hours of labor required to assemble one basket.
    \item $\text{material\_cost}$: Material cost per basket.
    \item $\text{selling\_price}$: Selling price per basket.
    \item $\text{holding\_cost}$: Holding cost per unsold basket at the end of each week.
    \item $\text{salvage\_value}$: Salvage value per unsold basket at the end of week $W$.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $\text{regular\_used}_{w}$: Hours of regular labor used in week $w$.
    \item $\text{overtime\_used}_{w}$: Hours of overtime labor used in week $w$.
    \item $\text{regular\_basket}_{w}$: Number of baskets assembled with regular labor in week $w$.
    \item $\text{overtime\_basket}_{w}$: Number of baskets assembled with overtime labor in week $w$.
    \item $\text{inventory}_{w}$: Number of baskets on hand at the end of week $w$.
\end{itemize}

\textbf{Objective:}

Maximize the total profit over the season:

\[
\begin{aligned}
\text{max} \quad & \sum_{w=1}^{W} \left( \text{selling\_price} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{regular\_cost} \times \text{regular\_used}_w \right. \\
& \left. - \text{overtime\_cost} \times \text{overtime\_used}_w - \text{material\_cost} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) \right. \\
& \left. - \text{holding\_cost} \times \text{inventory}_{w} \right) + \text{salvage\_value} \times \text{inventory}_{W}
\end{aligned}
\]

\textbf{Subject to:}

For each week $w = 1, \ldots, W$:

\begin{align*}
& \text{regular\_used}_{w} + \text{overtime\_used}_{w} \geq \text{assembly\_time} (\text{regular\_basket}_{w} + \text{overtime\_basket}_{w}) \\
& \text{regular\_used}_{w} \leq \text{regular\_labor}_{w} \\
& \text{overtime\_used}_{w} \leq \text{overtime\_labor}_{w} \\
& \text{inventory}_{w-1} + \text{regular\_basket}_{w} + \text{overtime\_basket}_{w} = \text{demand}_{w} + \text{inventory}_{w} \\
& \text{inventory}_{0} = 0
\end{align*}

All variables $\text{regular\_used}_{w}$, $\text{overtime\_used}_{w}$, $\text{regular\_basket}_{w}$, $\text{overtime\_basket}_{w}$, $\text{inventory}_{w}$ must be non-negative.

\end{document}
```

This model will help you determine the optimal decisions regarding labor utilization and inventory management to maximize the profit throughout the season.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\textbf{Given:}
\begin{itemize}
    \item $W$: Number of weeks in the season.
    \item $\text{demand}_{w}$: Demand for baskets in week $w$.
    \item $\text{regular\_labor}_{w}$: Maximum regular labor hours available in week $w$.
    \item $\text{regular\_cost}$: Cost per hour for regular labor.
    \item $\text{overtime\_labor}_{w}$: Maximum overtime labor hours available in week $w$.
    \item $\text{overtime\_cost}$: Cost per hour for overtime labor.
    \item $\text{assembly\_time}$: Hours of labor required to assemble one basket.
    \item $\text{material\_cost}$: Material cost per basket.
    \item $\text{selling\_price}$: Selling price per basket.
    \item $\text{holding\_cost}$: Holding cost per unsold basket at the end of each week.
    \item $\text{salvage\_value}$: Salvage value per unsold basket at the end of week $W$.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $\text{regular\_used}_{w}$: Hours of regular labor used in week $w$.
    \item $\text{overtime\_used}_{w}$: Hours of overtime labor used in week $w$.
    \item $\text{regular\_basket}_{w}$: Number of baskets assembled with regular labor in week $w$.
    \item $\text{overtime\_basket}_{w}$: Number of baskets assembled with overtime labor in week $w$.
    \item $\text{inventory}_{w}$: Number of baskets on hand at the end of week $w$.
\end{itemize}

\textbf{Objective:}

Maximize the total profit over the season:

\[
\begin{aligned}
\text{max} \quad & \sum_{w=1}^{W} \left( \text{selling\_price} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{regular\_cost} \times \text{regular\_used}_w \right. \\
& \left. - \text{overtime\_cost} \times \text{overtime\_used}_w - \text{material\_cost} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) \right. \\
& \left. - \text{holding\_cost} \times \text{inventory}_{w} \right) + \text{salvage\_value} \times \text{inventory}_{W}
\end{aligned}
\]

\textbf{Subject to:}

For each week $w = 1, \ldots, W$:

\begin{align*}
& \text{regular\_used}_{w} + \text{overtime\_used}_{w} \geq \text{assembly\_time} (\text{regular\_basket}_{w} + \text{overtime\_basket}_{w}) \\
& \text{regular\_used}_{w} \leq \text{regular\_labor}_{w} \\
& \text{overtime\_used}_{w} \leq \text{overtime\_labor}_{w} \\
& \text{inventory}_{w-1} + \text{regular\_basket}_{w} + \text{overtime\_basket}_{w} = \text{demand}_{w} + \text{inventory}_{w} \\
& \text{inventory}_{0} = 0
\end{align*}

All variables $\text{regular\_used}_{w}$, $\text{overtime\_used}_{w}$, $\text{regular\_basket}_{w}$, $\text{overtime\_basket}_{w}$, $\text{inventory}_{w}$ must be non-negative.

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data_json = '{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}'
data = json.loads(data_json)

#### Problem parameters
W = len(data['demand'])
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(W)]

#### Objective Function
profit_expr = pulp.lpSum(
    selling_price * (regular_basket[w] + overtime_basket[w]) -
    regular_cost * regular_used[w] -
    overtime_cost * overtime_used[w] -
    material_cost * (regular_basket[w] + overtime_basket[w]) -
    holding_cost * inventory[w]
    for w in range(W)
) + salvage_value * inventory[W-1]

problem += profit_expr

#### Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] >= assembly_time * (regular_basket[w] + overtime_basket[w])
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]
    if w > 0:
        problem += inventory[w-1] + regular_basket[w] + overtime_basket[w] == data['demand'][w] + inventory[w]

#### Initial inventory constraint
problem += inventory[0] == 0

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

