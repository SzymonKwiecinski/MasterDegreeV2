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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Steel Production}

\textbf{Variables:} \\
Let \( x_k \) be the amount of mineral \( k \) (in tons) melted, where \( k = 1, 2, \ldots, K \). \\
Let \( y \) be the amount of Manganese (Mn) directly added (in tons).

\textbf{Objective Function:} \\
Maximize profit:
\[
Z = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot x_k \right) - (melt\_price \cdot (x_1 + x_2 + \ldots + x_K)) - (mang\_price \cdot y)
\]

\textbf{Subject to:}

1. Steel Composition Constraints: \\
   - Manganese content:
   \[
   \frac{\sum_{k=1}^{K} (x_k \cdot contmn_k)}{n_{\text{steel\_quant}}} \geq \frac{mn_{\text{percent}}}{100}
   \]
   - Silicon content:
   \[
   \frac{\sum_{k=1}^{K} (x_k \cdot contsi_k)}{n_{\text{steel\_quant}}} \geq si_{\text{min}} \quad \text{and} \quad \frac{\sum_{k=1}^{K} (x_k \cdot contsi_k)}{n_{\text{steel\_quant}}} \leq si_{\text{max}}
   \]

2. Total Production Requirement:
\[
\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
\]

3. Non-negativity:
\[
x_k \geq 0 \quad \forall k \quad \text{and} \quad y \geq 0
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

\section*{Linear Programming Model for Steel Production}

\textbf{Variables:} \\
Let \( x_k \) be the amount of mineral \( k \) (in tons) melted, where \( k = 1, 2, \ldots, K \). \\
Let \( y \) be the amount of Manganese (Mn) directly added (in tons).

\textbf{Objective Function:} \\
Maximize profit:
\[
Z = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot x_k \right) - (melt\_price \cdot (x_1 + x_2 + \ldots + x_K)) - (mang\_price \cdot y)
\]

\textbf{Subject to:}

1. Steel Composition Constraints: \\
   - Manganese content:
   \[
   \frac{\sum_{k=1}^{K} (x_k \cdot contmn_k)}{n_{\text{steel\_quant}}} \geq \frac{mn_{\text{percent}}}{100}
   \]
   - Silicon content:
   \[
   \frac{\sum_{k=1}^{K} (x_k \cdot contsi_k)}{n_{\text{steel\_quant}}} \geq si_{\text{min}} \quad \text{and} \quad \frac{\sum_{k=1}^{K} (x_k \cdot contsi_k)}{n_{\text{steel\_quant}}} \leq si_{\text{max}}
   \]

2. Total Production Requirement:
\[
\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
\]

3. Non-negativity:
\[
x_k \geq 0 \quad \forall k \quad \text{and} \quad y \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from json
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

#### Unpack data
n_steel_quant = data['n_steel_quant']
mn_percent = data['mn_percent'] / 100
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']

#### Number of minerals
K = len(contsi)

#### Problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')

#### Objective Function
problem += (
    n_steel_quant * sell_price -
    pulp.lpSum([(cost[k] / 1000) * x[k] for k in range(K)]) -
    melt_price * pulp.lpSum(x) -
    mang_price * y
)

#### Constraints
#### Manganese content
problem += (
    pulp.lpSum([x[k] * contmn[k] for k in range(K)]) >= n_steel_quant * mn_percent
)

#### Silicon content
problem += (
    pulp.lpSum([x[k] * contsi[k] for k in range(K)]) >= n_steel_quant * si_min
)
problem += (
    pulp.lpSum([x[k] * contsi[k] for k in range(K)]) <= n_steel_quant * si_max
)

#### Total Production Requirement
problem += (
    pulp.lpSum(x) + y == n_steel_quant
)

#### Solve
problem.solve()

#### Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

