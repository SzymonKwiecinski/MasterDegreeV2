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

\section*{Mathematical Model}

\textbf{Parameters:}
\begin{itemize}
    \item \( W \): Number of weeks
    \item \( demand_w \): Demand in week \( w \)
    \item \( regular\_cost \): Cost of regular labor per hour
    \item \( overtime\_cost \): Cost of overtime labor per hour
    \item \( regular\_labor_w \): Available regular labor hours in week \( w \)
    \item \( overtime\_labor_w \): Available overtime labor hours in week \( w \)
    \item \( assembly\_time \): Time to assemble one basket
    \item \( material\_cost \): Cost of materials for one basket
    \item \( selling\_price \): Selling price for one basket
    \item \( holding\_cost \): Holding cost for unsold baskets
    \item \( salvage\_value \): Salvage value for unsold baskets at the end of week \( W \)
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item \( regular\_used_w \): Hours of regular labor used in week \( w \)
    \item \( overtime\_used_w \): Hours of overtime labor used in week \( w \)
    \item \( regular\_basket_w \): Number of baskets assembled with regular labor in week \( w \)
    \item \( overtime\_basket_w \): Number of baskets assembled with overtime labor in week \( w \)
    \item \( inventory_w \): Number of baskets on hand at the end of week \( w \)
\end{itemize}

\textbf{Objective Function:}
Maximize total profit:
\[
\text{Total Profit} = \sum_{w=1}^{W} \left( (regular\_basket_w + overtime\_basket_w) \cdot selling\_price - (regular\_used_w \cdot regular\_cost + overtime\_used_w \cdot overtime\_cost + regular\_basket_w \cdot material\_cost) - holding\_cost \cdot inventory_w - \begin{cases}
0 & \text{if } w < W \\
salvage\_value \cdot inventory_W & \text{if } w = W
\end{cases} \right)
\]

\textbf{Constraints:}
\begin{align*}
1. & \quad regular\_used_w \leq regular\_labor_w \quad \forall w \in \{1, \ldots, W\} \\
2. & \quad overtime\_used_w \leq overtime\_labor_w \quad \forall w \in \{1, \ldots, W\} \\
3. & \quad regular\_used_w + overtime\_used_w \geq assembly\_time \cdot (regular\_basket_w + overtime\_basket_w) \quad \forall w \in \{1, \ldots, W\} \\
4. & \quad inventory_{w-1} + regular\_basket_w + overtime\_basket_w - demand_w = inventory_w \quad \forall w \in \{1, \ldots, W\}, \quad inventory_0 = 0 \\
5. & \quad inventory_W \geq 0
\end{align*}

\textbf{Non-negativity:}
\begin{align*}
& regular\_used_w \geq 0, \quad overtime\_used_w \geq 0, \\
& regular\_basket_w \geq 0, \quad overtime\_basket_w \geq 0, \\
& inventory_w \geq 0 \quad \forall w \in \{1, \ldots, W\}
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

\section*{Mathematical Model}

\textbf{Parameters:}
\begin{itemize}
    \item \( W \): Number of weeks
    \item \( demand_w \): Demand in week \( w \)
    \item \( regular\_cost \): Cost of regular labor per hour
    \item \( overtime\_cost \): Cost of overtime labor per hour
    \item \( regular\_labor_w \): Available regular labor hours in week \( w \)
    \item \( overtime\_labor_w \): Available overtime labor hours in week \( w \)
    \item \( assembly\_time \): Time to assemble one basket
    \item \( material\_cost \): Cost of materials for one basket
    \item \( selling\_price \): Selling price for one basket
    \item \( holding\_cost \): Holding cost for unsold baskets
    \item \( salvage\_value \): Salvage value for unsold baskets at the end of week \( W \)
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item \( regular\_used_w \): Hours of regular labor used in week \( w \)
    \item \( overtime\_used_w \): Hours of overtime labor used in week \( w \)
    \item \( regular\_basket_w \): Number of baskets assembled with regular labor in week \( w \)
    \item \( overtime\_basket_w \): Number of baskets assembled with overtime labor in week \( w \)
    \item \( inventory_w \): Number of baskets on hand at the end of week \( w \)
\end{itemize}

\textbf{Objective Function:}
Maximize total profit:
\[
\text{Total Profit} = \sum_{w=1}^{W} \left( (regular\_basket_w + overtime\_basket_w) \cdot selling\_price - (regular\_used_w \cdot regular\_cost + overtime\_used_w \cdot overtime\_cost + regular\_basket_w \cdot material\_cost) - holding\_cost \cdot inventory_w - \begin{cases}
0 & \text{if } w < W \\
salvage\_value \cdot inventory_W & \text{if } w = W
\end{cases} \right)
\]

\textbf{Constraints:}
\begin{align*}
1. & \quad regular\_used_w \leq regular\_labor_w \quad \forall w \in \{1, \ldots, W\} \\
2. & \quad overtime\_used_w \leq overtime\_labor_w \quad \forall w \in \{1, \ldots, W\} \\
3. & \quad regular\_used_w + overtime\_used_w \geq assembly\_time \cdot (regular\_basket_w + overtime\_basket_w) \quad \forall w \in \{1, \ldots, W\} \\
4. & \quad inventory_{w-1} + regular\_basket_w + overtime\_basket_w - demand_w = inventory_w \quad \forall w \in \{1, \ldots, W\}, \quad inventory_0 = 0 \\
5. & \quad inventory_W \geq 0
\end{align*}

\textbf{Non-negativity:}
\begin{align*}
& regular\_used_w \geq 0, \quad overtime\_used_w \geq 0, \\
& regular\_basket_w \geq 0, \quad overtime\_basket_w \geq 0, \\
& inventory_w \geq 0 \quad \forall w \in \{1, \ldots, W\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads("{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}")

#### Parameters
W = len(data['demand'])
demand = data['demand']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(W), lowBound=0, cat='Integer')
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(W), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(W), lowBound=0)

#### Objective Function
profit = pulp.lpSum([
    (regular_basket[w] + overtime_basket[w]) * selling_price -
    (regular_used[w] * regular_cost + overtime_used[w] * overtime_cost + regular_basket[w] * material_cost) -
    holding_cost * inventory[w]
    for w in range(W)
]) + (salvage_value * inventory[W-1])

problem += profit

#### Constraints
for w in range(W):
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]
    problem += regular_used[w] + overtime_used[w] >= assembly_time * (regular_basket[w] + overtime_basket[w])
    if w == 0:
        problem += inventory[w] == regular_basket[w] + overtime_basket[w] - demand[w]
    else:
        problem += inventory[w] == inventory[w-1] + regular_basket[w] + overtime_basket[w] - demand[w]
    
problem += inventory[W-1] >= 0

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

