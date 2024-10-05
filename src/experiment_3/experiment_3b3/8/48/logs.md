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

\subsection*{Parameters}
\begin{align*}
& W: \text{Total number of weeks} \\
& demand_{w}: \text{Demand for week } w \\
& regular\_labor_{w}: \text{Available regular labor hours for week } w \\
& overtime\_labor_{w}: \text{Available overtime labor hours for week } w \\
& regular\_cost: \text{Cost of regular labor per hour} \\
& overtime\_cost: \text{Cost of overtime labor per hour} \\
& assembly\_time: \text{Time to assemble one basket (hours)} \\
& material\_cost: \text{Material cost for each basket} \\
& selling\_price: \text{Selling price for each basket} \\
& holding\_cost: \text{Holding cost for unsold baskets} \\
& salvage\_value: \text{Salvage value of unsold baskets at week } W
\end{align*}

\subsection*{Variables}
\begin{align*}
& regular\_used_{w}: \text{Hours of regular labor used in week } w \\
& overtime\_used_{w}: \text{Hours of overtime labor used in week } w \\
& regular\_baskets_{w}: \text{Number of baskets assembled with regular labor in week } w \\
& overtime\_baskets_{w}: \text{Number of baskets assembled with overtime labor in week } w \\
& inventory_{w}: \text{Number of baskets on hand at the end of week } w \\
& total\_profit: \text{Total profit for the season}
\end{align*}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{total\_profit} = \sum_{w=1}^{W} \left( (regular\_baskets_{w} + overtime\_baskets_{w}) \cdot selling\_price - (regular\_used_{w} \cdot regular\_cost + overtime\_used_{w} \cdot overtime\_cost + (regular\_baskets_{w} + overtime\_baskets_{w}) \cdot material\_cost + inventory_{w} \cdot holding\_cost) \right) + inventory_{W} \cdot salvage\_value
\]

\subsection*{Constraints}
\begin{align*}
& \text{1. Labor constraints:} \\
& regular\_used_{w} + overtime\_used_{w} \leq regular\_labor_{w} + overtime\_labor_{w}, \quad \forall w \in \{1, \dots, W\} \\

& \text{2. Demand fulfillment:} \\
& regular\_baskets_{w} + overtime\_baskets_{w} + inventory_{w-1} \geq demand_{w}, \quad \forall w \in \{1, \dots, W\} \\
& inventory_{w} = inventory_{w-1} + regular\_baskets_{w} + overtime\_baskets_{w} - demand_{w}, \quad \forall w \in \{1, \dots, W\} \\

& \text{3. Initial inventory:} \\
& inventory_{1} = 0 \\

& \text{4. Non-negativity constraints:} \\
& regular\_used_{w}, overtime\_used_{w}, regular\_baskets_{w}, overtime\_baskets_{w}, inventory_{w} \geq 0, \quad \forall w \in \{1, \dots, W\}
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

\subsection*{Parameters}
\begin{align*}
& W: \text{Total number of weeks} \\
& demand_{w}: \text{Demand for week } w \\
& regular\_labor_{w}: \text{Available regular labor hours for week } w \\
& overtime\_labor_{w}: \text{Available overtime labor hours for week } w \\
& regular\_cost: \text{Cost of regular labor per hour} \\
& overtime\_cost: \text{Cost of overtime labor per hour} \\
& assembly\_time: \text{Time to assemble one basket (hours)} \\
& material\_cost: \text{Material cost for each basket} \\
& selling\_price: \text{Selling price for each basket} \\
& holding\_cost: \text{Holding cost for unsold baskets} \\
& salvage\_value: \text{Salvage value of unsold baskets at week } W
\end{align*}

\subsection*{Variables}
\begin{align*}
& regular\_used_{w}: \text{Hours of regular labor used in week } w \\
& overtime\_used_{w}: \text{Hours of overtime labor used in week } w \\
& regular\_baskets_{w}: \text{Number of baskets assembled with regular labor in week } w \\
& overtime\_baskets_{w}: \text{Number of baskets assembled with overtime labor in week } w \\
& inventory_{w}: \text{Number of baskets on hand at the end of week } w \\
& total\_profit: \text{Total profit for the season}
\end{align*}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{total\_profit} = \sum_{w=1}^{W} \left( (regular\_baskets_{w} + overtime\_baskets_{w}) \cdot selling\_price - (regular\_used_{w} \cdot regular\_cost + overtime\_used_{w} \cdot overtime\_cost + (regular\_baskets_{w} + overtime\_baskets_{w}) \cdot material\_cost + inventory_{w} \cdot holding\_cost) \right) + inventory_{W} \cdot salvage\_value
\]

\subsection*{Constraints}
\begin{align*}
& \text{1. Labor constraints:} \\
& regular\_used_{w} + overtime\_used_{w} \leq regular\_labor_{w} + overtime\_labor_{w}, \quad \forall w \in \{1, \dots, W\} \\

& \text{2. Demand fulfillment:} \\
& regular\_baskets_{w} + overtime\_baskets_{w} + inventory_{w-1} \geq demand_{w}, \quad \forall w \in \{1, \dots, W\} \\
& inventory_{w} = inventory_{w-1} + regular\_baskets_{w} + overtime\_baskets_{w} - demand_{w}, \quad \forall w \in \{1, \dots, W\} \\

& \text{3. Initial inventory:} \\
& inventory_{1} = 0 \\

& \text{4. Non-negativity constraints:} \\
& regular\_used_{w}, overtime\_used_{w}, regular\_baskets_{w}, overtime\_baskets_{w}, inventory_{w} \geq 0, \quad \forall w \in \{1, \dots, W\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

#### Constants
W = len(data['demand'])

#### Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

#### Variables
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0) for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0) for w in range(W)]
regular_baskets = [pulp.LpVariable(f'regular_baskets_{w}', lowBound=0, cat='Integer') for w in range(W)]
overtime_baskets = [pulp.LpVariable(f'overtime_baskets_{w}', lowBound=0, cat='Integer') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Integer') for w in range(W)]

#### Objective Function
total_profit = (
    pulp.lpSum(
        (regular_baskets[w] + overtime_baskets[w]) * data['selling_price']
        - (regular_used[w] * data['regular_cost'] + overtime_used[w] * data['overtime_cost'])
        - (regular_baskets[w] + overtime_baskets[w]) * data['material_cost']
        - inventory[w] * data['holding_cost']
        for w in range(W)
    ) + inventory[W-1] * data['salvage_value']
)
problem += total_profit

#### Constraints

#### 1. Labor constraints
for w in range(W):
    problem += regular_used[w] + overtime_used[w] <= data['regular_labor'][w] + data['overtime_labor'][w]
    problem += regular_baskets[w] * data['assembly_time'] <= regular_used[w]
    problem += overtime_baskets[w] * data['assembly_time'] <= overtime_used[w]

#### 2. Demand fulfillment
for w in range(W):
    if w == 0:
        problem += regular_baskets[w] + overtime_baskets[w] >= data['demand'][w]
        continue
    problem += regular_baskets[w] + overtime_baskets[w] + inventory[w-1] >= data['demand'][w]
    problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w]

#### 3. Initial inventory
problem += inventory[0] == regular_baskets[0] + overtime_baskets[0] - data['demand'][0]

#### Solve the problem
problem.solve()

#### Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

