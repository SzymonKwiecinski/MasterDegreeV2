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
To model the problem of maximizing profit in the foundry, we need to establish decision variables, an objective function, and constraints. Here's the formulation in mathematical terms using Linear Programming:

######### Decision Variables
- \( x_k \): Amount of mineral \( k \) melted (in thousands of tons)
- \( y \): Amount of Manganese directly added (in tons)

######### Objective Function
The objective is to maximize profit, which is the revenue from selling the steel minus the costs of minerals, added manganese, and melting:

\[ \text{Profit} = \text{Revenue} - \text{Costs} \]

\[ \max \quad \text{Revenue} - \left( \sum_{k=1}^{K} \text{cost}_k \cdot x_k + \text{mang\_price} \cdot y + \text{melt\_price} \cdot n_{\text{steel\_quant}} \right) \]

Where:

\[ \text{Revenue} = \text{sell\_price} \cdot n_{\text{steel\_quant}} \]

######### Constraints
1. **Total Steel Quantity Constraint:**
   \[ \sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}} \]

2. **Manganese Content Constraint:**
   \[ \sum_{k=1}^{K} \text{contmn}_k \cdot x_k + y \geq \text{mn\_percent} \cdot n_{\text{steel\_quant}} \]

3. **Silicon Content Constraint:**
   \[ \text{si\_min} \cdot n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \text{contsi}_k \cdot x_k \leq \text{si\_max} \cdot n_{\text{steel\_quant}} \]

4. **Non-negativity Constraint:**
   \[ x_k \geq 0, \quad y \geq 0 \quad \text{for all } k \]

Now, let's put this formulation into LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\begin{align*}
x_k &: \text{Amount of mineral } k \text{ melted (in thousands of tons)} \\
y &: \text{Amount of Manganese directly added (in tons)}
\end{align*}

\textbf{Objective Function:}
\[
\max \left( \text{sell\_price} \cdot n_{\text{steel\_quant}} - \left( \sum_{k=1}^{K} \text{cost}_k \cdot x_k + \text{mang\_price} \cdot y + \text{melt\_price} \cdot n_{\text{steel\_quant}} \right) \right)
\]

\textbf{Subject to Constraints:}
\begin{align*}
&\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}} \\
&\sum_{k=1}^{K} \text{contmn}_k \cdot x_k + y \geq \text{mn\_percent} \cdot n_{\text{steel\_quant}} \\
&\text{si\_min} \cdot n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \text{contsi}_k \cdot x_k \leq \text{si\_max} \cdot n_{\text{steel\_quant}} \\
&x_k \geq 0 \quad \text{for all } k \\
&y \geq 0
\end{align*}

\end{document}
```

This linear programming model can be solved using any standard LP solver to determine the optimal values for \( x_k \) (amount of each mineral melted) and \( y \) (amount of Manganese added) that maximizes the profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\begin{align*}
x_k &: \text{Amount of mineral } k \text{ melted (in thousands of tons)} \\
y &: \text{Amount of Manganese directly added (in tons)}
\end{align*}

\textbf{Objective Function:}
\[
\max \left( \text{sell\_price} \cdot n_{\text{steel\_quant}} - \left( \sum_{k=1}^{K} \text{cost}_k \cdot x_k + \text{mang\_price} \cdot y + \text{melt\_price} \cdot n_{\text{steel\_quant}} \right) \right)
\]

\textbf{Subject to Constraints:}
\begin{align*}
&\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}} \\
&\sum_{k=1}^{K} \text{contmn}_k \cdot x_k + y \geq \text{mn\_percent} \cdot n_{\text{steel\_quant}} \\
&\text{si\_min} \cdot n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \text{contsi}_k \cdot x_k \leq \text{si\_max} \cdot n_{\text{steel\_quant}} \\
&x_k \geq 0 \quad \text{for all } k \\
&y \geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

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

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts('x', range(len(data['cost'])), lowBound=0, cat='Continuous')
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

#### Objective Function
problem += (
    data['sell_price'] * data['n_steel_quant'] 
    - (
        sum(data['cost'][k] * x[k] for k in range(len(data['cost']))) 
        + data['mang_price'] * y 
        + data['melt_price'] * data['n_steel_quant']
    )
)

#### Constraints
#### Total quantity constraint
problem += (
    sum(x[k] for k in range(len(data['cost']))) + y == data['n_steel_quant']
)

#### Manganese content constraint
problem += (
    sum(data['contmn'][k] * x[k] for k in range(len(data['contmn']))) + y >= data['mn_percent'] * data['n_steel_quant']
)

#### Silicon content constraints
problem += (
    data['si_min'] * data['n_steel_quant'] <= sum(data['contsi'][k] * x[k] for k in range(len(data['contsi'])))
)
problem += (
    sum(data['contsi'][k] * x[k] for k in range(len(data['contsi']))) <= data['si_max'] * data['n_steel_quant']
)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

