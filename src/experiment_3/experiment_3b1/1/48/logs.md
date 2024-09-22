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

\section*{Mathematical Model for Fine Foods Company}

\subsection*{Parameters}
\begin{align*}
W & : \text{Number of weeks} \\
\text{demand}_{w} & : \text{Demand for week } w, \quad w = 1, \ldots, W \\
\text{regular\_labor}_{w} & : \text{Regular labor hours available in week } w \\
\text{overtime\_labor}_{w} & : \text{Overtime labor hours available in week } w \\
\text{regular\_cost} & : \text{Cost of regular labor per hour} \\
\text{overtime\_cost} & : \text{Cost of overtime labor per hour} \\
\text{assembly\_time} & : \text{Time (hours) required to assemble one basket} \\
\text{material\_cost} & : \text{Material cost for one basket} \\
\text{selling\_price} & : \text{Selling price for one basket} \\
\text{holding\_cost} & : \text{Holding cost per unsold basket} \\
\text{salvage\_value} & : \text{Salvage value of unsold baskets at the end of the season}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{regular\_used}_{w} & : \text{Hours of regular labor used in week } w \\
\text{overtime\_used}_{w} & : \text{Hours of overtime labor used in week } w \\
\text{regular\_baskets}_{w} & : \text{Number of baskets assembled with regular labor in week } w \\
\text{overtime\_baskets}_{w} & : \text{Number of baskets assembled with overtime labor in week } w \\
\text{inventory}_{w} & : \text{Number of baskets on hand at the end of week } w \\
\text{total\_profit} & : \text{Total profit over the season}
\end{align*}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{total\_profit} = \sum_{w=1}^{W} \left( \text{selling\_price} \cdot (\text{regular\_baskets}_{w} + \text{overtime\_baskets}_{w}) - \text{material\_cost} \cdot (\text{regular\_baskets}_{w} + \text{overtime\_baskets}_{w}) - \text{regular\_cost} \cdot \text{regular\_used}_{w} - \text{overtime\_cost} \cdot \text{overtime\_used}_{w} - \text{holding\_cost} \cdot \text{inventory}_{w} \right)
\]

\subsection*{Constraints}
\begin{align}
\text{regular\_used}_{w} & \leq \text{regular\_labor}_{w} \quad \forall w \\
\text{overtime\_used}_{w} & \leq \text{overtime\_labor}_{w} \quad \forall w \\
\text{regular\_used}_{w} + \text{overtime\_used}_{w} & \geq \text{assembly\_time} \cdot (\text{regular\_baskets}_{w} + \text{overtime\_baskets}_{w}) \quad \forall w \\
\text{inventory}_{w} & = \text{inventory}_{w-1} + \text{regular\_baskets}_{w} + \text{overtime\_baskets}_{w} - \text{demand}_{w} \quad \forall w \\
\text{inventory}_{1} & = 0 \\
\text{inventory}_{W} & \text{ is eligible for salvage value, no holding cost}
\end{align}

\subsection*{Non-negativity Constraints}
\begin{align*}
\text{regular\_used}_{w} & \geq 0 \\
\text{overtime\_used}_{w} & \geq 0 \\
\text{regular\_baskets}_{w} & \geq 0 \\
\text{overtime\_baskets}_{w} & \geq 0 \\
\text{inventory}_{w} & \geq 0 \quad \forall w
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

\section*{Mathematical Model for Fine Foods Company}

\subsection*{Parameters}
\begin{align*}
W & : \text{Number of weeks} \\
\text{demand}_{w} & : \text{Demand for week } w, \quad w = 1, \ldots, W \\
\text{regular\_labor}_{w} & : \text{Regular labor hours available in week } w \\
\text{overtime\_labor}_{w} & : \text{Overtime labor hours available in week } w \\
\text{regular\_cost} & : \text{Cost of regular labor per hour} \\
\text{overtime\_cost} & : \text{Cost of overtime labor per hour} \\
\text{assembly\_time} & : \text{Time (hours) required to assemble one basket} \\
\text{material\_cost} & : \text{Material cost for one basket} \\
\text{selling\_price} & : \text{Selling price for one basket} \\
\text{holding\_cost} & : \text{Holding cost per unsold basket} \\
\text{salvage\_value} & : \text{Salvage value of unsold baskets at the end of the season}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{regular\_used}_{w} & : \text{Hours of regular labor used in week } w \\
\text{overtime\_used}_{w} & : \text{Hours of overtime labor used in week } w \\
\text{regular\_baskets}_{w} & : \text{Number of baskets assembled with regular labor in week } w \\
\text{overtime\_baskets}_{w} & : \text{Number of baskets assembled with overtime labor in week } w \\
\text{inventory}_{w} & : \text{Number of baskets on hand at the end of week } w \\
\text{total\_profit} & : \text{Total profit over the season}
\end{align*}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{total\_profit} = \sum_{w=1}^{W} \left( \text{selling\_price} \cdot (\text{regular\_baskets}_{w} + \text{overtime\_baskets}_{w}) - \text{material\_cost} \cdot (\text{regular\_baskets}_{w} + \text{overtime\_baskets}_{w}) - \text{regular\_cost} \cdot \text{regular\_used}_{w} - \text{overtime\_cost} \cdot \text{overtime\_used}_{w} - \text{holding\_cost} \cdot \text{inventory}_{w} \right)
\]

\subsection*{Constraints}
\begin{align}
\text{regular\_used}_{w} & \leq \text{regular\_labor}_{w} \quad \forall w \\
\text{overtime\_used}_{w} & \leq \text{overtime\_labor}_{w} \quad \forall w \\
\text{regular\_used}_{w} + \text{overtime\_used}_{w} & \geq \text{assembly\_time} \cdot (\text{regular\_baskets}_{w} + \text{overtime\_baskets}_{w}) \quad \forall w \\
\text{inventory}_{w} & = \text{inventory}_{w-1} + \text{regular\_baskets}_{w} + \text{overtime\_baskets}_{w} - \text{demand}_{w} \quad \forall w \\
\text{inventory}_{1} & = 0 \\
\text{inventory}_{W} & \text{ is eligible for salvage value, no holding cost}
\end{align}

\subsection*{Non-negativity Constraints}
\begin{align*}
\text{regular\_used}_{w} & \geq 0 \\
\text{overtime\_used}_{w} & \geq 0 \\
\text{regular\_baskets}_{w} & \geq 0 \\
\text{overtime\_baskets}_{w} & \geq 0 \\
\text{inventory}_{w} & \geq 0 \quad \forall w
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
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
selling_price = data['selling_price']
material_cost = data['material_cost']
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
holding_cost = data['holding_cost']
assembly_time = data['assembly_time']

#### Initialize the problem
problem = pulp.LpProblem("Fine_Foods_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
regular_used = pulp.LpVariable.dicts("RegularUsed", range(W), 0)
overtime_used = pulp.LpVariable.dicts("OvertimeUsed", range(W), 0)
regular_baskets = pulp.LpVariable.dicts("RegularBaskets", range(W), 0, None, pulp.LpInteger)
overtime_baskets = pulp.LpVariable.dicts("OvertimeBaskets", range(W), 0, None, pulp.LpInteger)
inventory = pulp.LpVariable.dicts("Inventory", range(W), 0)

#### Objective Function
total_profit = pulp.lpSum(
    (selling_price * (regular_baskets[w] + overtime_baskets[w]) -
     material_cost * (regular_baskets[w] + overtime_baskets[w]) -
     regular_cost * regular_used[w] -
     overtime_cost * overtime_used[w] -
     holding_cost * inventory[w]) for w in range(W)
)

problem += total_profit

#### Constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]
    problem += regular_used[w] + overtime_used[w] >= assembly_time * (regular_baskets[w] + overtime_baskets[w])
    
    if w > 0:
        problem += inventory[w] == inventory[w-1] + regular_baskets[w] + overtime_baskets[w] - data['demand'][w]
    else:
        problem += inventory[w] == regular_baskets[w] + overtime_baskets[w] - data['demand'][w]

#### Initial inventory constraint
problem += inventory[0] == 0 

#### Last week inventory does not incur holding cost
#### No additional constraint is needed as it is implicitly handled

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

