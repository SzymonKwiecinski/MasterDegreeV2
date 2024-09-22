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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Alloy Production}

\textbf{Parameters:}
\begin{itemize}
    \item $A$: Total weight of the alloy to be produced (in lb)
    \item $M$: Total number of metals
    \item $K$: Total number of available alloys
    \item $target_{m}$: Target quantity of metal $m$ in the alloy
    \item $ratio_{k,m}$: Ratio of metal $m$ in alloy $k$
    \item $price_{k}$: Price of alloy $k$
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $amount_{k}$: Amount of alloy $k$ to be purchased
\end{itemize}

\textbf{Objective:}
Minimize the total cost of the alloys:
\begin{equation}
\text{Minimize } Z = \sum_{k=1}^{K} price_{k} \cdot amount_{k}
\end{equation}

\textbf{Subject to:}
\begin{itemize}
    \item Total weight constraint:
    \begin{equation}
    \sum_{k=1}^{K} amount_{k} = A
    \end{equation}

    \item Metal composition constraints for each metal $m$:
    \begin{equation}
    \sum_{k=1}^{K} ratio_{k,m} \cdot amount_{k} = target_{m}, \quad \forall m = 1, 2, \ldots, M
    \end{equation}

    \item Non-negativity constraints:
    \begin{equation}
    amount_{k} \geq 0, \quad \forall k = 1, 2, \ldots, K
    \end{equation}
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

\section*{Linear Programming Model for Alloy Production}

\textbf{Parameters:}
\begin{itemize}
    \item $A$: Total weight of the alloy to be produced (in lb)
    \item $M$: Total number of metals
    \item $K$: Total number of available alloys
    \item $target_{m}$: Target quantity of metal $m$ in the alloy
    \item $ratio_{k,m}$: Ratio of metal $m$ in alloy $k$
    \item $price_{k}$: Price of alloy $k$
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $amount_{k}$: Amount of alloy $k$ to be purchased
\end{itemize}

\textbf{Objective:}
Minimize the total cost of the alloys:
\begin{equation}
\text{Minimize } Z = \sum_{k=1}^{K} price_{k} \cdot amount_{k}
\end{equation}

\textbf{Subject to:}
\begin{itemize}
    \item Total weight constraint:
    \begin{equation}
    \sum_{k=1}^{K} amount_{k} = A
    \end{equation}

    \item Metal composition constraints for each metal $m$:
    \begin{equation}
    \sum_{k=1}^{K} ratio_{k,m} \cdot amount_{k} = target_{m}, \quad \forall m = 1, 2, \ldots, M
    \end{equation}

    \item Non-negativity constraints:
    \begin{equation}
    amount_{k} \geq 0, \quad \forall k = 1, 2, \ldots, K
    \end{equation}
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

A = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

#### Define the problem
problem = pulp.LpProblem("Alloy_Production_Optimization", pulp.LpMinimize)

#### Define variables
K = len(price)
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

#### Total weight constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == A, "Total_Weight"

#### Metal composition constraints
for m in range(len(target)):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_Composition_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

