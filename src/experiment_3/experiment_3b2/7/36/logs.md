# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A manufacturer wishes to produce \var{alloy_quant} lb of an alloy that consists of several kinds of metals.
- And by weight, the alloy we want contains a target quantity\var{target_{m}} of metal \var{metal_{m}}.
- Several other kinds of alloys are available at various prices. 
- These alloys can be melted to get the alloy we want.
- Alloy \var{k} has \var{ratio_{k, m}} ratio of \var{metal_{m}} and is sold at price of \var{price_k}.
- Ratio \var{ratio_{k, m}} ranges between 0 and 1.0 and should be properly treated in optimization

INPUT FORMAT:

{
	"alloy_quant": alloy_quant,
	"target": [target_{m} for m in 1,...,M],
	"ratio": [[ratio_{k, m} for m in 1,...,M] for k = 1,...,K],
	"price": [price_{k} for k in 1,...,K]
}

OBJECTIVE: The manufacturer wishes to find the amounts of the various alloys needed and to determine the cheapest combination.

OUTPUT INFO:

- \var{amount} represents the quantity of each alloy we buy

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate this problem as a Linear Programming (LP) model, we need to determine the amount of each available alloy that should be melted together to meet the target weights of metals specified, while minimizing the cost.

Let's define the variables and constraints:

- Let \( x_k \) be the amount of alloy \( k \) purchased, for \( k = 1, \ldots, K \).

The objective is to minimize the total cost:

\[ \text{Minimize} \quad \sum_{k=1}^{K} price_k \times x_k \]

Subject to the following constraints:

1. Metal composition constraints: For each metal \( m \),

   \[ \sum_{k=1}^{K} ratio_{k, m} \times x_k = target_m \times alloy\_quant \]

2. Total alloy quantity constraint:

   \[ \sum_{k=1}^{K} x_k = alloy\_quant \]

3. Non-negativity constraints:

   \[ x_k \geq 0 \quad \text{for all } k \]

Here is the complete formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Objective:}
Minimize the total cost of alloys:

\begin{equation}
\text{Minimize} \quad \sum_{k=1}^{K} price_k \times x_k
\end{equation}

\subsection*{Subject to:}

\subsubsection*{Metal Composition Constraints:}
For each metal \( m \),

\begin{equation}
\sum_{k=1}^{K} ratio_{k, m} \times x_k = target_m \times alloy\_quant \quad \text{for } m = 1, \ldots, M
\end{equation}

\subsubsection*{Total Alloy Quantity Constraint:}
\begin{equation}
\sum_{k=1}^{K} x_k = alloy\_quant
\end{equation}

\subsubsection*{Non-negativity Constraints:}
\begin{equation}
x_k \geq 0 \quad \text{for all } k
\end{equation}

\end{document}
```

This LP model will help determine the optimal amounts of each alloy to purchase so that the desired alloy composition is achieved at the minimum cost. Each constraint ensures that the metals' weights and total quantity meet the specified requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Objective:}
Minimize the total cost of alloys:

\begin{equation}
\text{Minimize} \quad \sum_{k=1}^{K} price_k \times x_k
\end{equation}

\subsection*{Subject to:}

\subsubsection*{Metal Composition Constraints:}
For each metal \( m \),

\begin{equation}
\sum_{k=1}^{K} ratio_{k, m} \times x_k = target_m \times alloy\_quant \quad \text{for } m = 1, \ldots, M
\end{equation}

\subsubsection*{Total Alloy Quantity Constraint:}
\begin{equation}
\sum_{k=1}^{K} x_k = alloy\_quant
\end{equation}

\subsubsection*{Non-negativity Constraints:}
\begin{equation}
x_k \geq 0 \quad \text{for all } k
\end{equation}

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

#### Number of alloys and metals
K = len(price)
M = len(target)

#### Create the problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum([price[k] * x[k] for k in range(K)])

#### Metal Composition Constraints
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * x[k] for k in range(K)]) == target[m] * alloy_quant

#### Total Alloy Quantity Constraint
problem += pulp.lpSum([x[k] for k in range(K)]) == alloy_quant

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

