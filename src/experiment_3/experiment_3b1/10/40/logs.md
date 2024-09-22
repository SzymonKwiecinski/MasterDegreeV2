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

Let:
\begin{itemize}
    \item \( x_k \) = amount of mineral \( k \) melted (in tons) for \( k = 1, 2, \ldots, K \)
    \item \( y \) = amount of Manganese added (in tons)
\end{itemize}

\textbf{Objective Function:}
Maximize Profit, \( Z \):
\[
Z = n_{steel\_quant} \times sell\_price - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \times x_k + melt\_price \times x_k \right) - mang\_price \times y
\]

\textbf{Subject to:}

1. Manganese content constraint:
\[
\frac{\sum_{k=1}^{K} cont_{mn_k} \times x_k + y}{n_{steel\_quant}} \geq \frac{mn\_percent}{100}
\]

2. Silicon content constraints:
\[
\frac{\sum_{k=1}^{K} cont_{si_k} \times x_k}{n_{steel\_quant}} \geq \frac{si_{min}}{100}
\]
\[
\frac{\sum_{k=1}^{K} cont_{si_k} \times x_k}{n_{steel\_quant}} \leq \frac{si_{max}}{100}
\]

3. Non-negativity constraints:
\[
x_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]
\[
y \geq 0
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

Let:
\begin{itemize}
    \item \( x_k \) = amount of mineral \( k \) melted (in tons) for \( k = 1, 2, \ldots, K \)
    \item \( y \) = amount of Manganese added (in tons)
\end{itemize}

\textbf{Objective Function:}
Maximize Profit, \( Z \):
\[
Z = n_{steel\_quant} \times sell\_price - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \times x_k + melt\_price \times x_k \right) - mang\_price \times y
\]

\textbf{Subject to:}

1. Manganese content constraint:
\[
\frac{\sum_{k=1}^{K} cont_{mn_k} \times x_k + y}{n_{steel\_quant}} \geq \frac{mn\_percent}{100}
\]

2. Silicon content constraints:
\[
\frac{\sum_{k=1}^{K} cont_{si_k} \times x_k}{n_{steel\_quant}} \geq \frac{si_{min}}{100}
\]
\[
\frac{\sum_{k=1}^{K} cont_{si_k} \times x_k}{n_{steel\_quant}} \leq \frac{si_{max}}{100}
\]

3. Non-negativity constraints:
\[
x_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]
\[
y \geq 0
\]

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

#### Define the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision Variables
K = len(data['contsi'])
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### amount of mineral k melted
y = pulp.LpVariable("y", lowBound=0)  #### amount of Manganese added

#### Objective Function
profit = (data['n_steel_quant'] * data['sell_price'] - 
          pulp.lpSum((data['cost'][k] / 1000) * x[k] + data['melt_price'] * x[k] for k in range(K)) - 
          data['mang_price'] * y)

problem += profit, "Total_Profit"

#### Constraints
#### Manganese content constraint
problem += (pulp.lpSum(data['contmn'][k] * x[k] for k in range(K)) + y) >= (data['mn_percent'] / 100) * data['n_steel_quant'], "Mn_Content_Constraint"

#### Silicon content constraints
problem += (pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) / data['n_steel_quant']) >= (data['si_min'] / 100), "Si_Min_Constraint"
problem += (pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) / data['n_steel_quant']) <= (data['si_max'] / 100), "Si_Max_Constraint"

#### Solve the problem
problem.solve()

#### Printing the outcome
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

