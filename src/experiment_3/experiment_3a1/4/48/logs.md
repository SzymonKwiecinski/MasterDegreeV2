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

\textbf{Variables:}
\begin{itemize}
    \item Let \( \text{regular\_used}_w \) be the hours of regular labor used in week \( w \).
    \item Let \( \text{overtime\_used}_w \) be the hours of overtime labor used in week \( w \).
    \item Let \( \text{regular\_basket}_w \) be the number of baskets assembled with regular labor in week \( w \).
    \item Let \( \text{overtime\_basket}_w \) be the number of baskets assembled with overtime labor in week \( w \).
    \item Let \( \text{inventory}_w \) be the number of baskets on hand at the end of week \( w \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( W \): Total number of weeks
    \item \( \text{demand}_w \): Demand for week \( w \)
    \item \( \text{regular\_labor}_w \): Available regular labor hours in week \( w \)
    \item \( \text{overtime\_labor}_w \): Available overtime labor hours in week \( w \)
    \item \( \text{assembly\_time} \): Time required to assemble one basket
    \item \( \text{regular\_cost} \): Cost of regular labor per hour
    \item \( \text{overtime\_cost} \): Cost of overtime labor per hour
    \item \( \text{material\_cost} \): Material cost for each basket
    \item \( \text{selling\_price} \): Selling price of each basket
    \item \( \text{holding\_cost} \): Holding cost per unsold basket
    \item \( \text{salvage\_value} \): Salvage value of unsold baskets at the end of week \( W \)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{w=1}^{W} \left( \text{selling\_price} \cdot (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{regular\_cost} \cdot \text{regular\_used}_w - \text{overtime\_cost} \cdot \text{overtime\_used}_w - \text{material\_cost} \cdot (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{holding\_cost} \cdot \text{inventory}_w \right) + \text{salvage\_value} \cdot \text{inventory}_W
\]

\textbf{Constraints:}
\begin{align*}
    & \text{Regular Labor:} \quad \text{regular\_used}_w \leq \text{regular\_labor}_w, \quad \forall w \\
    & \text{Overtime Labor:} \quad \text{overtime\_used}_w \leq \text{overtime\_labor}_w, \quad \forall w \\
    & \text{Assembly Time Constraint:} \quad \text{regular\_used}_w + \text{overtime\_used}_w \geq \text{assembly\_time} \cdot (\text{regular\_basket}_w + \text{overtime\_basket}_w), \quad \forall w \\
    & \text{Demand Constraint:} \quad \text{regular\_basket}_w + \text{overtime\_basket}_w + \text{inventory}_{w-1} = \text{demand}_w + \text{inventory}_w, \quad \forall w \text{ where } w > 1 \\
    & \text{Initial Inventory:} \quad \text{inventory}_1 = 0 \\
    & \text{Final Inventory Salvage:} \quad \text{inventory}_W \geq 0 \\
    & \text{Non-negativity Constraints:} \quad \text{regular\_used}_w, \text{overtime\_used}_w, \text{regular\_basket}_w, \text{overtime\_basket}_w, \text{inventory}_w \geq 0, \quad \forall w
\end{align*}

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{regular\_used} = [\text{regular\_used}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{overtime\_used} = [\text{overtime\_used}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{regular\_baskets} = [\text{regular\_basket}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{overtime\_baskets} = [\text{overtime\_basket}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{inventory} = [\text{inventory}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{total\_profit} = Z \)
\end{itemize}

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

\textbf{Variables:}
\begin{itemize}
    \item Let \( \text{regular\_used}_w \) be the hours of regular labor used in week \( w \).
    \item Let \( \text{overtime\_used}_w \) be the hours of overtime labor used in week \( w \).
    \item Let \( \text{regular\_basket}_w \) be the number of baskets assembled with regular labor in week \( w \).
    \item Let \( \text{overtime\_basket}_w \) be the number of baskets assembled with overtime labor in week \( w \).
    \item Let \( \text{inventory}_w \) be the number of baskets on hand at the end of week \( w \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( W \): Total number of weeks
    \item \( \text{demand}_w \): Demand for week \( w \)
    \item \( \text{regular\_labor}_w \): Available regular labor hours in week \( w \)
    \item \( \text{overtime\_labor}_w \): Available overtime labor hours in week \( w \)
    \item \( \text{assembly\_time} \): Time required to assemble one basket
    \item \( \text{regular\_cost} \): Cost of regular labor per hour
    \item \( \text{overtime\_cost} \): Cost of overtime labor per hour
    \item \( \text{material\_cost} \): Material cost for each basket
    \item \( \text{selling\_price} \): Selling price of each basket
    \item \( \text{holding\_cost} \): Holding cost per unsold basket
    \item \( \text{salvage\_value} \): Salvage value of unsold baskets at the end of week \( W \)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{w=1}^{W} \left( \text{selling\_price} \cdot (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{regular\_cost} \cdot \text{regular\_used}_w - \text{overtime\_cost} \cdot \text{overtime\_used}_w - \text{material\_cost} \cdot (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{holding\_cost} \cdot \text{inventory}_w \right) + \text{salvage\_value} \cdot \text{inventory}_W
\]

\textbf{Constraints:}
\begin{align*}
    & \text{Regular Labor:} \quad \text{regular\_used}_w \leq \text{regular\_labor}_w, \quad \forall w \\
    & \text{Overtime Labor:} \quad \text{overtime\_used}_w \leq \text{overtime\_labor}_w, \quad \forall w \\
    & \text{Assembly Time Constraint:} \quad \text{regular\_used}_w + \text{overtime\_used}_w \geq \text{assembly\_time} \cdot (\text{regular\_basket}_w + \text{overtime\_basket}_w), \quad \forall w \\
    & \text{Demand Constraint:} \quad \text{regular\_basket}_w + \text{overtime\_basket}_w + \text{inventory}_{w-1} = \text{demand}_w + \text{inventory}_w, \quad \forall w \text{ where } w > 1 \\
    & \text{Initial Inventory:} \quad \text{inventory}_1 = 0 \\
    & \text{Final Inventory Salvage:} \quad \text{inventory}_W \geq 0 \\
    & \text{Non-negativity Constraints:} \quad \text{regular\_used}_w, \text{overtime\_used}_w, \text{regular\_basket}_w, \text{overtime\_basket}_w, \text{inventory}_w \geq 0, \quad \forall w
\end{align*}

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{regular\_used} = [\text{regular\_used}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{overtime\_used} = [\text{overtime\_used}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{regular\_baskets} = [\text{regular\_basket}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{overtime\_baskets} = [\text{overtime\_basket}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{inventory} = [\text{inventory}_w \text{ for } w = 1, \ldots, W] \)
    \item \( \text{total\_profit} = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = json.loads('{"regular_cost": 30, "overtime_cost": 45, "assembly_time": 0.4, "material_cost": 25, "selling_price": 65, "holding_cost": 4, "salvage_value": 30, "demand": [700, 1500, 2800, 1800], "regular_labor": [450, 550, 600, 600], "overtime_labor": [40, 200, 320, 160]}')

#### Assigning parameters from data
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

#### Initialize the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

#### Decision Variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(1, W + 1), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(1, W + 1), lowBound=0)
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(1, W + 1), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(1, W + 1), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(1, W + 1), lowBound=0)

#### Objective Function
problem += pulp.lpSum([
    selling_price * (regular_basket[w] + overtime_basket[w]) 
    - regular_cost * regular_used[w] 
    - overtime_cost * overtime_used[w] 
    - material_cost * (regular_basket[w] + overtime_basket[w]) 
    - holding_cost * inventory[w] 
    for w in range(1, W + 1)
]) + salvage_value * inventory[W], "Total_Profit"

#### Constraints
for w in range(1, W + 1):
    problem += regular_used[w] <= regular_labor[w - 1], f"Regular_Labor_Constraint_{w}"
    problem += overtime_used[w] <= overtime_labor[w - 1], f"Overtime_Labor_Constraint_{w}"
    problem += regular_used[w] + overtime_used[w] >= assembly_time * (regular_basket[w] + overtime_basket[w]), f"Assembly_Time_Constraint_{w}"

for w in range(2, W + 1):
    problem += regular_basket[w] + overtime_basket[w] + inventory[w - 1] == demand[w - 1] + inventory[w], f"Demand_Constraint_{w}"

problem += inventory[1] == 0, "Initial_Inventory"
problem += inventory[W] >= 0, "Final_Inventory_Salvage"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

