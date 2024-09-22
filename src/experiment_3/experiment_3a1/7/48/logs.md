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

\section*{Linear Programming Model for Gift Basket Production}

\subsection*{Indices}
\begin{itemize}
    \item $w$: Week index, where $w = 1, \ldots, W$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $W$: Total number of weeks
    \item $demand_{w}$: Demand for baskets in week $w$
    \item $regular\_labor_{w}$: Available regular labor hours in week $w$
    \item $overtime\_labor_{w}$: Available overtime labor hours in week $w$
    \item $regular\_cost$: Cost of regular labor per hour
    \item $overtime\_cost$: Cost of overtime labor per hour
    \item $assembly\_time$: Time in hours to assemble one basket
    \item $material\_cost$: Material cost for each basket
    \item $selling\_price$: Selling price for each basket
    \item $holding\_cost$: Holding cost for unsold baskets
    \item $salvage\_value$: Salvage value of unsold baskets at the end of week $W$
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $regular\_used_{w}$: Hours of regular labor used in week $w$
    \item $overtime\_used_{w}$: Hours of overtime labor used in week $w$
    \item $regular\_baskets_{w}$: Number of baskets assembled using regular labor in week $w$
    \item $overtime\_baskets_{w}$: Number of baskets assembled using overtime labor in week $w$
    \item $inventory_{w}$: Number of baskets on hand at the end of week $w$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:

\begin{align*}
    \text{Total Profit} = \sum_{w=1}^{W} \left( (selling\_price \cdot (regular\_baskets_{w} + overtime\_baskets_{w})) - (regular\_cost \cdot regular\_used_{w}) - (overtime\_cost \cdot overtime\_used_{w}) - (material\_cost \cdot (regular\_baskets_{w} + overtime\_baskets_{w})) - (holding\_cost \cdot inventory_{w}) \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
    & \text{Production Capacity Constraints:} \\
    & regular\_used_{w} + overtime\_used_{w} \leq regular\_labor_{w} + overtime\_labor_{w} \quad \forall w \\
    & \text{Basket Assembly Constraints:} \\
    & regular\_baskets_{w} \cdot assembly\_time \leq regular\_used_{w} \\
    & overtime\_baskets_{w} \cdot assembly\_time \leq overtime\_used_{w} \\
    & \text{Demand Satisfaction Constraints:} \\
    & regular\_baskets_{w} + overtime\_baskets_{w} + inventory_{w-1} = demand_{w} + inventory_{w} \quad \forall w = 2, \ldots, W \\
    & inventory_{1} = 0 \\
    & \text{Salvage Value Condition:} \\
    & inventory_{W} \text{ incurs salvage value} \\
    & \text{Non-negativity Constraints:} \\
    & regular\_used_{w} \geq 0, \quad overtime\_used_{w} \geq 0, \\
    & regular\_baskets_{w} \geq 0, \quad overtime\_baskets_{w} \geq 0, \\
    & inventory_{w} \geq 0 \quad \forall w
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

\section*{Linear Programming Model for Gift Basket Production}

\subsection*{Indices}
\begin{itemize}
    \item $w$: Week index, where $w = 1, \ldots, W$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $W$: Total number of weeks
    \item $demand_{w}$: Demand for baskets in week $w$
    \item $regular\_labor_{w}$: Available regular labor hours in week $w$
    \item $overtime\_labor_{w}$: Available overtime labor hours in week $w$
    \item $regular\_cost$: Cost of regular labor per hour
    \item $overtime\_cost$: Cost of overtime labor per hour
    \item $assembly\_time$: Time in hours to assemble one basket
    \item $material\_cost$: Material cost for each basket
    \item $selling\_price$: Selling price for each basket
    \item $holding\_cost$: Holding cost for unsold baskets
    \item $salvage\_value$: Salvage value of unsold baskets at the end of week $W$
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $regular\_used_{w}$: Hours of regular labor used in week $w$
    \item $overtime\_used_{w}$: Hours of overtime labor used in week $w$
    \item $regular\_baskets_{w}$: Number of baskets assembled using regular labor in week $w$
    \item $overtime\_baskets_{w}$: Number of baskets assembled using overtime labor in week $w$
    \item $inventory_{w}$: Number of baskets on hand at the end of week $w$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:

\begin{align*}
    \text{Total Profit} = \sum_{w=1}^{W} \left( (selling\_price \cdot (regular\_baskets_{w} + overtime\_baskets_{w})) - (regular\_cost \cdot regular\_used_{w}) - (overtime\_cost \cdot overtime\_used_{w}) - (material\_cost \cdot (regular\_baskets_{w} + overtime\_baskets_{w})) - (holding\_cost \cdot inventory_{w}) \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
    & \text{Production Capacity Constraints:} \\
    & regular\_used_{w} + overtime\_used_{w} \leq regular\_labor_{w} + overtime\_labor_{w} \quad \forall w \\
    & \text{Basket Assembly Constraints:} \\
    & regular\_baskets_{w} \cdot assembly\_time \leq regular\_used_{w} \\
    & overtime\_baskets_{w} \cdot assembly\_time \leq overtime\_used_{w} \\
    & \text{Demand Satisfaction Constraints:} \\
    & regular\_baskets_{w} + overtime\_baskets_{w} + inventory_{w-1} = demand_{w} + inventory_{w} \quad \forall w = 2, \ldots, W \\
    & inventory_{1} = 0 \\
    & \text{Salvage Value Condition:} \\
    & inventory_{W} \text{ incurs salvage value} \\
    & \text{Non-negativity Constraints:} \\
    & regular\_used_{w} \geq 0, \quad overtime\_used_{w} \geq 0, \\
    & regular\_baskets_{w} \geq 0, \quad overtime\_baskets_{w} \geq 0, \\
    & inventory_{w} \geq 0 \quad \forall w
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
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

#### Create the LP problem
problem = pulp.LpProblem("GiftBasketProduction", pulp.LpMaximize)

#### Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(1, W + 1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(1, W + 1), lowBound=0)
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(1, W + 1), lowBound=0)
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(1, W + 1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(1, W + 1), lowBound=0)

#### Objective Function
profit = pulp.lpSum([(selling_price * (regular_baskets[w] + overtime_baskets[w])) -
                     (regular_cost * regular_used[w]) -
                     (overtime_cost * overtime_used[w]) -
                     (material_cost * (regular_baskets[w] + overtime_baskets[w])) -
                     (holding_cost * inventory[w]) for w in range(1, W + 1)])

problem += profit

#### Constraints
for w in range(1, W + 1):
    #### Production Capacity Constraints
    problem += regular_used[w] + overtime_used[w] <= regular_labor[w - 1] + overtime_labor[w - 1]
    
    #### Basket Assembly Constraints
    problem += regular_baskets[w] * assembly_time <= regular_used[w]
    problem += overtime_baskets[w] * assembly_time <= overtime_used[w]
    
    #### Demand Satisfaction Constraints
    if w > 1:
        problem += regular_baskets[w] + overtime_baskets[w] + inventory[w - 1] == demand[w - 1] + inventory[w]
    
    #### Initial inventory condition
    if w == 1:
        problem += inventory[1] == 0

#### Salvage Value Condition
problem += inventory[W] >= 0  #### Inventory at week W incurs salvage value

#### Non-negativity Constraints are inherently handled by lowBound=0 in variable declarations

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

