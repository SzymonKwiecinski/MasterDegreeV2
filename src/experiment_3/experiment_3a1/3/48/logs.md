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

\section*{Mathematical Model for the Gift Basket Production Problem}

\textbf{Variables:}

\begin{itemize}
    \item $regular\_used_{w}$: hours of regular labor used in week $w$.
    \item $overtime\_used_{w}$: hours of overtime labor used in week $w$.
    \item $regular\_basket_{w}$: number of baskets assembled with regular labor in week $w$.
    \item $overtime\_basket_{w}$: number of baskets assembled with overtime labor in week $w$.
    \item $inventory_{w}$: number of baskets on hand at the end of week $w$.
\end{itemize}

\textbf{Parameters:}

\begin{itemize}
    \item $W$: total number of weeks.
    \item $demand_{w}$: demand in week $w$.
    \item $regular\_labor_{w}$: available regular labor hours in week $w$.
    \item $overtime\_labor_{w}$: available overtime labor hours in week $w$.
    \item $assembly\_time$: hours of labor required to assemble one basket.
    \item $regular\_cost$: cost of regular labor per hour.
    \item $overtime\_cost$: cost of overtime labor per hour.
    \item $material\_cost$: material cost for each basket.
    \item $selling\_price$: selling price for each basket.
    \item $holding\_cost$: holding cost for unsold baskets.
    \item $salvage\_value$: salvage value for unsold baskets at the end of $W$.
\end{itemize}

\textbf{Objective Function:}

Maximize total profit:

\[
\text{Maximize } Z = \sum_{w=1}^{W} \left( (selling\_price - material\_cost) \cdot (regular\_basket_{w} + overtime\_basket_{w}) - regular\_cost \cdot regular\_used_{w} - overtime\_cost \cdot overtime\_used_{w} - holding\_cost \cdot inventory_{w} \right) + salvage\_value \cdot inventory_{W}
\]

\textbf{Constraints:}

1. Labor Constraints:
    \[
    regular\_used_{w} + overtime\_used_{w} \leq regular\_labor_{w} + overtime\_labor_{w}, \quad \forall w = 1, \ldots, W
    \]

2. Assembly Constraints:
    \[
    regular\_basket_{w} + overtime\_basket_{w} \leq \frac{regular\_used_{w}}{assembly\_time} + \frac{overtime\_used_{w}}{assembly\_time}, \quad \forall w = 1, \ldots, W
    \]

3. Demand Fulfillment:
    \[
    inventory_{w-1} + regular\_basket_{w} + overtime\_basket_{w} - demand_{w} = inventory_{w}, \quad \forall w = 1, \ldots, W
    \]
    with $inventory_{0} = 0$.

4. Non-negativity Constraints:
    \[
    regular\_used_{w} \geq 0, \quad overtime\_used_{w} \geq 0, \quad regular\_basket_{w} \geq 0, \quad overtime\_basket_{w} \geq 0, \quad inventory_{w} \geq 0, \quad \forall w = 1, \ldots, W
    \]

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

\section*{Mathematical Model for the Gift Basket Production Problem}

\textbf{Variables:}

\begin{itemize}
    \item $regular\_used_{w}$: hours of regular labor used in week $w$.
    \item $overtime\_used_{w}$: hours of overtime labor used in week $w$.
    \item $regular\_basket_{w}$: number of baskets assembled with regular labor in week $w$.
    \item $overtime\_basket_{w}$: number of baskets assembled with overtime labor in week $w$.
    \item $inventory_{w}$: number of baskets on hand at the end of week $w$.
\end{itemize}

\textbf{Parameters:}

\begin{itemize}
    \item $W$: total number of weeks.
    \item $demand_{w}$: demand in week $w$.
    \item $regular\_labor_{w}$: available regular labor hours in week $w$.
    \item $overtime\_labor_{w}$: available overtime labor hours in week $w$.
    \item $assembly\_time$: hours of labor required to assemble one basket.
    \item $regular\_cost$: cost of regular labor per hour.
    \item $overtime\_cost$: cost of overtime labor per hour.
    \item $material\_cost$: material cost for each basket.
    \item $selling\_price$: selling price for each basket.
    \item $holding\_cost$: holding cost for unsold baskets.
    \item $salvage\_value$: salvage value for unsold baskets at the end of $W$.
\end{itemize}

\textbf{Objective Function:}

Maximize total profit:

\[
\text{Maximize } Z = \sum_{w=1}^{W} \left( (selling\_price - material\_cost) \cdot (regular\_basket_{w} + overtime\_basket_{w}) - regular\_cost \cdot regular\_used_{w} - overtime\_cost \cdot overtime\_used_{w} - holding\_cost \cdot inventory_{w} \right) + salvage\_value \cdot inventory_{W}
\]

\textbf{Constraints:}

1. Labor Constraints:
    \[
    regular\_used_{w} + overtime\_used_{w} \leq regular\_labor_{w} + overtime\_labor_{w}, \quad \forall w = 1, \ldots, W
    \]

2. Assembly Constraints:
    \[
    regular\_basket_{w} + overtime\_basket_{w} \leq \frac{regular\_used_{w}}{assembly\_time} + \frac{overtime\_used_{w}}{assembly\_time}, \quad \forall w = 1, \ldots, W
    \]

3. Demand Fulfillment:
    \[
    inventory_{w-1} + regular\_basket_{w} + overtime\_basket_{w} - demand_{w} = inventory_{w}, \quad \forall w = 1, \ldots, W
    \]
    with $inventory_{0} = 0$.

4. Non-negativity Constraints:
    \[
    regular\_used_{w} \geq 0, \quad overtime\_used_{w} \geq 0, \quad regular\_basket_{w} \geq 0, \quad overtime\_basket_{w} \geq 0, \quad inventory_{w} \geq 0, \quad \forall w = 1, \ldots, W
    \]

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
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

#### Create a linear programming problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

#### Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("RegularBasket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("OvertimeBasket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

#### Objective Function
profit = pulp.lpSum([
    (data['selling_price'] - data['material_cost']) * (regular_basket[w] + overtime_basket[w]) -
    data['regular_cost'] * regular_used[w] -
    data['overtime_cost'] * overtime_used[w] -
    data['holding_cost'] * inventory[w]
    for w in range(W)
])
profit += data['salvage_value'] * inventory[W-1]
problem += profit, "Total_Profit"

#### Constraints
for w in range(W):
    #### Labor Constraints
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w], f"Labor_Constraint_{w}"

    #### Assembly Constraints
    problem += regular_basket[w] + overtime_basket[w] <= (regular_used[w] + overtime_used[w]) / data['assembly_time'], f"Assembly_Constraint_{w}"

    #### Inventory Constraints
    if w == 0:
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - data['demand'][w], f"Inventory_Constraint_{w}"
    else:
        problem += inventory[w-1] + regular_basket[w] + overtime_basket[w] - data['demand'][w] == inventory[w], f"Inventory_Constraint_{w}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

