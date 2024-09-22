# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A foundry receives a specific order for \var{n_steel_quant} tons of steel. 
- This steel must meet the following characteristics: it must contain at least \var{mn_percent} percentage of manganese (Mn) while its percentage of silicon (SI) must be between \var{si_min} and \var{si_max}.
- To cast this steel, the foundry has limited quantities of several types of minerals.
- The contents expressed in percentage per mineral \var{k} are \var{contsi_{k}} for Si and \var{contmn_{k}} for Mn.
- The process for producing steel is such that direct addition of Mn is possible.
- This Manganese is available at a price of \var{mang_price} million euros per ton. 
- As for the minerals, it costs \var{cost_{k}} million euros per thousand tons for mineral \var{k}.
- The foundry plans to sell the steel produced at \var{sell_price} million euros per ton.
- The cost of smelting a ton of mineral is \var{melt_price} million euros.

INPUT FORMAT:

{
	"n_steel_quant": n_steel_quant,
	"mn_percent": mn_percent,
	"si_min": si_min,
	"si_max": si_max,
	"contsi": [contsi_{k} for k in 1,...,K]
	"contmn": [contmn_{k} for k in 1,...,K]
	"mang_price": mang_price,
	"cost": [cost_{k} for k in 1,...,K]
	"sell_price": sell_price,
	"melt_price": melt_price
}

OBJECTIVE: How should the manufacture manage the steel to maximize profit?

OUTPUT INFO:

- \var{amount} represents the amount of each mineral melted
- \var{num_mang} represents the amount of Manganese directly added

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
	"num_mang": [num_mang]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this problem as a linear programming problem in LaTeX, you need to formulate the objective function and constraints properly.

Given the information in the problem, the objective is to maximize profit, which is the difference between the revenue from selling the steel and the production cost, including the melting cost and the cost of additional manganese.

Here's the LaTeX formulation of this linear programming problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Objective:} Maximize profit

\begin{align*}
\text{Maximize: } & Z = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \times \text{amount}_k \right) - \text{mang\_price} \times \text{num\_mang} - \text{melt\_price} \times \sum_{k=1}^{K} \text{amount}_k
\end{align*}

\textbf{Subject to:}

\begin{align*}
1. & \quad \text{Total manganese requirement:} \\
& \sum_{k=1}^{K} \text{contmn}_k \times \text{amount}_k + \text{num\_mang} = \text{mn\_percent} \times \text{n\_steel\_quant} \\
2. & \quad \text{Total silicon requirement (lower bound):} \\
& \sum_{k=1}^{K} \text{contsi}_k \times \text{amount}_k \geq \text{si\_min} \times \text{n\_steel\_quant} \\
3. & \quad \text{Total silicon requirement (upper bound):} \\
& \sum_{k=1}^{K} \text{contsi}_k \times \text{amount}_k \leq \text{si\_max} \times \text{n\_steel\_quant} \\
4. & \quad \text{Total mass of minerals:} \\
& \sum_{k=1}^{K} \text{amount}_k = \text{n\_steel\_quant} \\
5. & \quad \text{Non-negativity constraints:} \\
& \text{amount}_k \geq 0 \quad \text{for all } k = 1, \ldots, K \\
& \text{num\_mang} \geq 0
\end{align*}

\end{document}
```

This formulation captures the objective function to maximize profit, considering the cost of minerals and manganese addition, as well as smelting. The constraints ensure that the steel produced meets the manganese and silicon content requirements, and that the total amount of minerals used equals the total steel demand. Non-negativity constraints ensure that all decision variables are non-negative.

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

\textbf{Objective:} Maximize profit

\begin{align*}
\text{Maximize: } & Z = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \times \text{amount}_k \right) - \text{mang\_price} \times \text{num\_mang} - \text{melt\_price} \times \sum_{k=1}^{K} \text{amount}_k
\end{align*}

\textbf{Subject to:}

\begin{align*}
1. & \quad \text{Total manganese requirement:} \\
& \sum_{k=1}^{K} \text{contmn}_k \times \text{amount}_k + \text{num\_mang} = \text{mn\_percent} \times \text{n\_steel\_quant} \\
2. & \quad \text{Total silicon requirement (lower bound):} \\
& \sum_{k=1}^{K} \text{contsi}_k \times \text{amount}_k \geq \text{si\_min} \times \text{n\_steel\_quant} \\
3. & \quad \text{Total silicon requirement (upper bound):} \\
& \sum_{k=1}^{K} \text{contsi}_k \times \text{amount}_k \leq \text{si\_max} \times \text{n\_steel\_quant} \\
4. & \quad \text{Total mass of minerals:} \\
& \sum_{k=1}^{K} \text{amount}_k = \text{n\_steel\_quant} \\
5. & \quad \text{Non-negativity constraints:} \\
& \text{amount}_k \geq 0 \quad \text{for all } k = 1, \ldots, K \\
& \text{num\_mang} \geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Data
data = {
    'n_steel_quant': 1000, 
    'mn_percent': 0.45, 
    'si_min': 3.25, 
    'si_max': 5.0, 
    'contsi': [4.0, 1.0, 0.6], 
    'contmn': [0.45, 0.5, 0.4], 
    'mang_price': 8.0, 
    'cost': [21, 25, 15], 
    'sell_price': 0.45, 
    'melt_price': 0.005
}

K = len(data['contsi'])

#### Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

#### Objective function
problem += (
    data['sell_price'] * data['n_steel_quant'] 
    - sum((data['cost'][k] / 1000) * amount[k] for k in range(K))
    - data['mang_price'] * num_mang
    - data['melt_price'] * sum(amount[k] for k in range(K))
), "Objective"

#### Constraints
problem += (
    sum(data['contmn'][k] * amount[k] for k in range(K)) + num_mang 
    == data['mn_percent'] * data['n_steel_quant']
), "Manganese Requirement"

problem += (
    sum(data['contsi'][k] * amount[k] for k in range(K)) 
    >= data['si_min'] * data['n_steel_quant']
), "Silicon Lower Bound Requirement"

problem += (
    sum(data['contsi'][k] * amount[k] for k in range(K)) 
    <= data['si_max'] * data['n_steel_quant']
), "Silicon Upper Bound Requirement"

problem += (
    sum(amount[k] for k in range(K)) 
    == data['n_steel_quant']
), "Total Mass of Minerals"

#### Solve the problem
problem.solve()

#### Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

