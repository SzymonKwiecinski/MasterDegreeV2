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
To model this problem as a linear program, we will define decision variables, constraints, and the objective function.

######### Decision Variables

Let \( x_k \) represent the amount (in thousand tons) of mineral \( k \) used.  
Let \( y \) represent the amount (in tons) of Manganese directly added.

######### Objective Function

We want to maximize the profit, which is calculated as revenue from selling the steel minus the costs of minerals, Manganese, and melting.

The objective function can be expressed as:

\[
\text{Maximize: } z = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} \left( \text{cost}_{k} \cdot x_k + \text{melt\_price} \cdot x_k \right) - \text{mang\_price} \cdot y
\]

######### Constraints

1. **Total Steel Production Constraint:**
   \[
   \sum_{k=1}^{K} x_k = \frac{n_{\text{steel\_quant}}}{1000}
   \]
   This ensures that the total amount of minerals used equals the required amount of steel, considering that `x_k` is measured in thousand tons.

2. **Manganese Content Constraint:**
   \[
   \sum_{k=1}^{K} \left(\text{contmn}_{k} \cdot x_k \right) + y \geq \frac{\text{mn\_percent}}{100} \cdot n_{\text{steel\_quant}}
   \]
   This ensures that the manganese content is at least `mn_percent`.

3. **Silicon Content Constraints:**
   \[
   \frac{\text{si\_min}}{100} \cdot n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \left( \text{contsi}_{k} \cdot x_k \right) \leq \frac{\text{si\_max}}{100} \cdot n_{\text{steel\_quant}}
   \]
   This ensures that the silicon content is within the specified bounds.

4. **Non-negativity Constraints:**
   \[
   x_k \geq 0 \quad \forall k
   \]
   \[
   y \geq 0
   \]

Here is the complete mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Objective:}
\[
\text{Maximize: } z = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} \left( \text{cost}_{k} \cdot x_k + \text{melt\_price} \cdot x_k \right) - \text{mang\_price} \cdot y
\]

\textbf{Subject to:}

\begin{enumerate}
    \item Total Steel Production Constraint:
    \[
    \sum_{k=1}^{K} x_k = \frac{n_{\text{steel\_quant}}}{1000}
    \]

    \item Manganese Content Constraint:
    \[
    \sum_{k=1}^{K} \left(\text{contmn}_{k} \cdot x_k \right) + y \geq \frac{\text{mn\_percent}}{100} \cdot n_{\text{steel\_quant}}
    \]

    \item Silicon Content Constraints:
    \[
    \frac{\text{si\_min}}{100} \cdot n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \left( \text{contsi}_{k} \cdot x_k \right) \leq \frac{\text{si\_max}}{100} \cdot n_{\text{steel\_quant}}
    \]

    \item Non-negativity Constraints:
    \[
    x_k \geq 0 \quad \forall k
    \]
    \[
    y \geq 0
    \]
\end{enumerate}

\end{document}
```

This linear program will provide the optimal amounts of each mineral and manganese addition to maximize profit while meeting the steel production specifications.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Objective:}
\[
\text{Maximize: } z = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} \left( \text{cost}_{k} \cdot x_k + \text{melt\_price} \cdot x_k \right) - \text{mang\_price} \cdot y
\]

\textbf{Subject to:}

\begin{enumerate}
    \item Total Steel Production Constraint:
    \[
    \sum_{k=1}^{K} x_k = \frac{n_{\text{steel\_quant}}}{1000}
    \]

    \item Manganese Content Constraint:
    \[
    \sum_{k=1}^{K} \left(\text{contmn}_{k} \cdot x_k \right) + y \geq \frac{\text{mn\_percent}}{100} \cdot n_{\text{steel\_quant}}
    \]

    \item Silicon Content Constraints:
    \[
    \frac{\text{si\_min}}{100} \cdot n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \left( \text{contsi}_{k} \cdot x_k \right) \leq \frac{\text{si\_max}}{100} \cdot n_{\text{steel\_quant}}
    \]

    \item Non-negativity Constraints:
    \[
    x_k \geq 0 \quad \forall k
    \]
    \[
    y \geq 0
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from the provided JSON
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

#### Number of types of metal
K = len(data['cost'])

#### Initialize the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Define decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(K)]
y = pulp.LpVariable('y', lowBound=0)

#### Objective function
objective = (data['n_steel_quant'] * data['sell_price']
             - sum((data['cost'][k] + data['melt_price']) * x[k] for k in range(K))
             - data['mang_price'] * y)
problem += objective

#### Constraint 1: Total Steel Production Constraint
problem += pulp.lpSum(x[k] for k in range(K)) == data['n_steel_quant'] / 1000

#### Constraint 2: Manganese Content Constraint
problem += pulp.lpSum(data['contmn'][k] * x[k] for k in range(K)) + y >= (data['mn_percent'] / 100) * data['n_steel_quant']

#### Constraint 3: Silicon Content Constraints
problem += pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) >= (data['si_min'] / 100) * data['n_steel_quant']
problem += pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) <= (data['si_max'] / 100) * data['n_steel_quant']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

