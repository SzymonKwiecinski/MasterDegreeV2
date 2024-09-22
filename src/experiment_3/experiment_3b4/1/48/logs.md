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
To model this problem, we will define the decision variables and formulate the objective function and constraints in a Linear Programming model. The goal is to maximize the total profit over the season, considering the costs and constraints related to labor and inventory management.

Let's define the decision variables:

- \( \text{regular\_used}_w \): Hours of regular labor used in week \( w \).
- \( \text{overtime\_used}_w \): Hours of overtime labor used in week \( w \).
- \( \text{regular\_basket}_w \): Number of baskets assembled with regular labor in week \( w \).
- \( \text{overtime\_basket}_w \): Number of baskets assembled with overtime labor in week \( w \).
- \( \text{inventory}_w \): Number of baskets on hand at the end of week \( w \).

The objective is to maximize the total profit over the season:

\[
\text{Total Profit} = \sum_{w=1}^{W} \left( \text{selling\_price} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{regular\_cost} \times \text{regular\_used}_w - \text{overtime\_cost} \times \text{overtime\_used}_w - \text{material\_cost} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{holding\_cost} \times \text{inventory}_w \right) + \text{salvage\_value} \times \text{inventory}_W
\]

Subject to the following constraints:

1. Labor constraints:

   \[
   \text{assembly\_time} \times \text{regular\_basket}_w = \text{regular\_used}_w, \quad \forall w
   \]
   \[
   \text{assembly\_time} \times \text{overtime\_basket}_w = \text{overtime\_used}_w, \quad \forall w
   \]

2. Demand and inventory balance:

   \[
   \text{regular\_basket}_w + \text{overtime\_basket}_w + \text{inventory}_{w-1} = \text{demand}_w + \text{inventory}_w, \quad \forall w
   \]

   For week 1:

   \[
   \text{inventory}_0 = 0
   \]

3. Labor availability constraints:

   \[
   0 \leq \text{regular\_used}_w \leq \text{regular\_labor}_w, \quad \forall w
   \]
   \[
   0 \leq \text{overtime\_used}_w \leq \text{overtime\_labor}_w, \quad \forall w
   \]

Now, let's convert this problem into a LaTeX document with the LP model structure:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Maximize the total profit:

\[
\text{Total Profit} = \sum_{w=1}^{W} \left( \text{selling\_price} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{regular\_cost} \times \text{regular\_used}_w - \text{overtime\_cost} \times \text{overtime\_used}_w \right.
\]
\[
\left. - \text{material\_cost} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{holding\_cost} \times \text{inventory}_w \right) + \text{salvage\_value} \times \text{inventory}_W
\]

\subsection*{Constraints}

1. Labor constraints:
\[
\text{assembly\_time} \times \text{regular\_basket}_w = \text{regular\_used}_w, \quad \forall w
\]
\[
\text{assembly\_time} \times \text{overtime\_basket}_w = \text{overtime\_used}_w, \quad \forall w
\]

2. Demand and inventory balance:
\[
\text{regular\_basket}_w + \text{overtime\_basket}_w + \text{inventory}_{w-1} = \text{demand}_w + \text{inventory}_w, \quad \forall w
\]

For week 1:
\[
\text{inventory}_0 = 0
\]

3. Labor availability constraints:
\[
0 \leq \text{regular\_used}_w \leq \text{regular\_labor}_w, \quad \forall w
\]
\[
0 \leq \text{overtime\_used}_w \leq \text{overtime\_labor}_w, \quad \forall w
\]

\end{document}
```

This LaTeX representation includes the objective function and all the necessary constraints for the problem described. Make sure to replace the placeholder variables with actual data or decision variables as needed.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Maximize the total profit:

\[
\text{Total Profit} = \sum_{w=1}^{W} \left( \text{selling\_price} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{regular\_cost} \times \text{regular\_used}_w - \text{overtime\_cost} \times \text{overtime\_used}_w \right.
\]
\[
\left. - \text{material\_cost} \times (\text{regular\_basket}_w + \text{overtime\_basket}_w) - \text{holding\_cost} \times \text{inventory}_w \right) + \text{salvage\_value} \times \text{inventory}_W
\]

\subsection*{Constraints}

1. Labor constraints:
\[
\text{assembly\_time} \times \text{regular\_basket}_w = \text{regular\_used}_w, \quad \forall w
\]
\[
\text{assembly\_time} \times \text{overtime\_basket}_w = \text{overtime\_used}_w, \quad \forall w
\]

2. Demand and inventory balance:
\[
\text{regular\_basket}_w + \text{overtime\_basket}_w + \text{inventory}_{w-1} = \text{demand}_w + \text{inventory}_w, \quad \forall w
\]

For week 1:
\[
\text{inventory}_0 = 0
\]

3. Labor availability constraints:
\[
0 \leq \text{regular\_used}_w \leq \text{regular\_labor}_w, \quad \forall w
\]
\[
0 \leq \text{overtime\_used}_w \leq \text{overtime\_labor}_w, \quad \forall w
\]

\end{document}</MATH_MODEL>
<DATA>
{'regular_cost': 30, 'overtime_cost': 45, 'assembly_time': 0.4, 'material_cost': 25, 'selling_price': 65, 'holding_cost': 4, 'salvage_value': 30, 'demand': [700, 1500, 2800, 1800], 'regular_labor': [450, 550, 600, 600], 'overtime_labor': [40, 200, 320, 160]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Create a LP maximization problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

#### Decision variables
regular_basket = [pulp.LpVariable(f'regular_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
overtime_basket = [pulp.LpVariable(f'overtime_basket_{w}', lowBound=0, cat='Continuous') for w in range(W)]
inventory = [pulp.LpVariable(f'inventory_{w}', lowBound=0, cat='Continuous') for w in range(W)]
regular_used = [pulp.LpVariable(f'regular_used_{w}', lowBound=0, cat='Continuous') for w in range(W)]
overtime_used = [pulp.LpVariable(f'overtime_used_{w}', lowBound=0, cat='Continuous') for w in range(W)]

#### Objective function
total_profit = (
    pulp.lpSum([
        data['selling_price'] * (regular_basket[w] + overtime_basket[w])
        - data['regular_cost'] * regular_used[w]
        - data['overtime_cost'] * overtime_used[w]
        - data['material_cost'] * (regular_basket[w] + overtime_basket[w])
        - data['holding_cost'] * inventory[w]
        for w in range(W)
    ]) + data['salvage_value'] * inventory[W-1]
)
problem += total_profit

#### Constraints
#### 1. Labor constraints
for w in range(W):
    problem += data['assembly_time'] * regular_basket[w] == regular_used[w]
    problem += data['assembly_time'] * overtime_basket[w] == overtime_used[w]

#### 2. Demand and inventory balance
problem += inventory[0] == 0
for w in range(W):
    if w == 0:
        prev_inventory = 0  #### For week 1
    else:
        prev_inventory = inventory[w-1]
    problem += regular_basket[w] + overtime_basket[w] + prev_inventory == data['demand'][w] + inventory[w]

#### 3. Labor availability constraints
for w in range(W):
    problem += regular_used[w] <= data['regular_labor'][w]
    problem += overtime_used[w] <= data['overtime_labor'][w]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

