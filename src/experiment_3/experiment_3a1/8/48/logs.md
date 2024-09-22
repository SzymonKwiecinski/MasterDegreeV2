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

\textbf{Parameters:}
\begin{itemize}
    \item $W$: Number of weeks
    \item $demand_{w}$: Demand for week $w$, for $w = 1, \ldots, W$
    \item $regular\_labor_{w}$: Regular labor hours available in week $w$
    \item $overtime\_labor_{w}$: Overtime labor hours available in week $w$
    \item $assembly\_time$: Hours required to assemble one basket
    \item $regular\_cost$: Cost per hour for regular labor
    \item $overtime\_cost$: Cost per hour for overtime labor
    \item $material\_cost$: Cost of materials for one basket
    \item $selling\_price$: Selling price for one basket
    \item $holding\_cost$: Holding cost per unsold basket
    \item $salvage\_value$: Salvage value for unsold baskets at week $W$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $regular\_used_{w}$: Hours of regular labor used in week $w$
    \item $overtime\_used_{w}$: Hours of overtime labor used in week $w$
    \item $regular\_basket_{w}$: Number of baskets assembled with regular labor in week $w$
    \item $overtime\_basket_{w}$: Number of baskets assembled with overtime labor in week $w$
    \item $inventory_{w}$: Number of baskets on hand at the end of week $w$
\end{itemize}

\textbf{Objective Function:}
Maximize total profit:
\[
\text{total\_profit} = \sum_{w=1}^{W} \left( (selling\_price \cdot (regular\_basket_{w} + overtime\_basket_{w})) - (regular\_cost \cdot regular\_used_{w}) - (overtime\_cost \cdot overtime\_used_{w}) - (material\_cost \cdot (regular\_basket_{w} + overtime\_basket_{w})) - (holding\_cost \cdot inventory_{w}) \right) + salvage\_value \cdot inventory_{W}
\]

\textbf{Constraints:}
\begin{align*}
1. & \quad regular\_used_{w} + overtime\_used_{w} \leq regular\_labor_{w} + overtime\_labor_{w}, \quad \forall w = 1, \ldots, W \\
2. & \quad regular\_basket_{w} = \frac{regular\_used_{w}}{assembly\_time}, \quad \forall w = 1, \ldots, W \\
3. & \quad overtime\_basket_{w} = \frac{overtime\_used_{w}}{assembly\_time}, \quad \forall w = 1, \ldots, W \\
4. & \quad inventory_{w} = inventory_{w-1} + regular\_basket_{w} + overtime\_basket_{w} - demand_{w}, \quad \forall w = 2, \ldots, W \\
5. & \quad inventory_{1} = 0 \\
6. & \quad inventory_{W} \geq 0 \\
7. & \quad regular\_used_{w} \geq 0, \quad \forall w = 1, \ldots, W \\
8. & \quad overtime\_used_{w} \geq 0, \quad \forall w = 1, \ldots, W \\
9. & \quad regular\_basket_{w} \geq 0, \quad \forall w = 1, \ldots, W \\
10. & \quad overtime\_basket_{w} \geq 0, \quad \forall w = 1, \ldots, W \\
11. & \quad inventory_{w} \geq 0, \quad \forall w = 1, \ldots, W
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

\textbf{Parameters:}
\begin{itemize}
    \item $W$: Number of weeks
    \item $demand_{w}$: Demand for week $w$, for $w = 1, \ldots, W$
    \item $regular\_labor_{w}$: Regular labor hours available in week $w$
    \item $overtime\_labor_{w}$: Overtime labor hours available in week $w$
    \item $assembly\_time$: Hours required to assemble one basket
    \item $regular\_cost$: Cost per hour for regular labor
    \item $overtime\_cost$: Cost per hour for overtime labor
    \item $material\_cost$: Cost of materials for one basket
    \item $selling\_price$: Selling price for one basket
    \item $holding\_cost$: Holding cost per unsold basket
    \item $salvage\_value$: Salvage value for unsold baskets at week $W$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $regular\_used_{w}$: Hours of regular labor used in week $w$
    \item $overtime\_used_{w}$: Hours of overtime labor used in week $w$
    \item $regular\_basket_{w}$: Number of baskets assembled with regular labor in week $w$
    \item $overtime\_basket_{w}$: Number of baskets assembled with overtime labor in week $w$
    \item $inventory_{w}$: Number of baskets on hand at the end of week $w$
\end{itemize}

\textbf{Objective Function:}
Maximize total profit:
\[
\text{total\_profit} = \sum_{w=1}^{W} \left( (selling\_price \cdot (regular\_basket_{w} + overtime\_basket_{w})) - (regular\_cost \cdot regular\_used_{w}) - (overtime\_cost \cdot overtime\_used_{w}) - (material\_cost \cdot (regular\_basket_{w} + overtime\_basket_{w})) - (holding\_cost \cdot inventory_{w}) \right) + salvage\_value \cdot inventory_{W}
\]

\textbf{Constraints:}
\begin{align*}
1. & \quad regular\_used_{w} + overtime\_used_{w} \leq regular\_labor_{w} + overtime\_labor_{w}, \quad \forall w = 1, \ldots, W \\
2. & \quad regular\_basket_{w} = \frac{regular\_used_{w}}{assembly\_time}, \quad \forall w = 1, \ldots, W \\
3. & \quad overtime\_basket_{w} = \frac{overtime\_used_{w}}{assembly\_time}, \quad \forall w = 1, \ldots, W \\
4. & \quad inventory_{w} = inventory_{w-1} + regular\_basket_{w} + overtime\_basket_{w} - demand_{w}, \quad \forall w = 2, \ldots, W \\
5. & \quad inventory_{1} = 0 \\
6. & \quad inventory_{W} \geq 0 \\
7. & \quad regular\_used_{w} \geq 0, \quad \forall w = 1, \ldots, W \\
8. & \quad overtime\_used_{w} \geq 0, \quad \forall w = 1, \ldots, W \\
9. & \quad regular\_basket_{w} \geq 0, \quad \forall w = 1, \ldots, W \\
10. & \quad overtime\_basket_{w} \geq 0, \quad \forall w = 1, \ldots, W \\
11. & \quad inventory_{w} \geq 0, \quad \forall w = 1, \ldots, W
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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

W = len(data['demand'])

#### Define the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

#### Decision variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(1, W + 1)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(1, W + 1)]
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0) for w in range(1, W + 1)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0) for w in range(1, W + 1)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0) for w in range(1, W + 1)]

#### Objective function
total_profit = pulp.lpSum(
    (
        data['selling_price'] * (regular_basket[w] + overtime_basket[w]) 
        - data['regular_cost'] * regular_used[w] 
        - data['overtime_cost'] * overtime_used[w] 
        - data['material_cost'] * (regular_basket[w] + overtime_basket[w]) 
        - data['holding_cost'] * inventory[w]
    ) for w in range(W)
) + (data['salvage_value'] * inventory[W - 1])
problem += total_profit

#### Constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w]

for w in range(W):
    problem += regular_basket[w] == regular_used[w] / data['assembly_time']
    problem += overtime_basket[w] == overtime_used[w] / data['assembly_time']

for w in range(1, W):
    problem += inventory[w] == inventory[w - 1] + regular_basket[w] + overtime_basket[w] - data['demand'][w]

#### Initial inventory for week 1
problem += inventory[0] == 0

#### Non-negativity constraints are already enforced by defining the variables with lowBound=0

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

