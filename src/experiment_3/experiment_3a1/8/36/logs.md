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

\section*{Linear Programming Model}

\textbf{Parameters:}
\begin{itemize}
    \item $A$: Total amount of alloy to be produced (in lb), $A = \text{alloy\_quant}$
    \item $M$: Number of metals in the alloy
    \item $K$: Number of available alloys
    \item $t_m$: Target quantity of metal $m$, $t_m = \text{target}_m$ for $m = 1, \ldots, M$
    \item $r_{k,m}$: Ratio of metal $m$ in alloy $k$, where $k = 1, \ldots, K$ and $m = 1, \ldots, M$
    \item $p_k$: Price of alloy $k$, where $k = 1, \ldots, K$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_k$: Amount of alloy $k$ to be purchased (in lb), for $k = 1, \ldots, K$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{k=1}^{K} p_k x_k
\]

\textbf{Subject to:}
\begin{align}
    \sum_{k=1}^{K} x_k &= A \quad \text{(Total amount of alloy)} \\
    \sum_{k=1}^{K} r_{k,m} x_k &\geq t_m \quad \text{for } m = 1, \ldots, M \quad \text{(Metal requirements)} \\
    x_k &\geq 0 \quad \text{for } k = 1, \ldots, K \quad \text{(Non-negativity constraint)}
\end{align}

\textbf{Output:}
The solution will provide the quantities of each alloy to purchase:
\[
\text{amount} = [x_1, x_2, \ldots, x_K]
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

\section*{Linear Programming Model}

\textbf{Parameters:}
\begin{itemize}
    \item $A$: Total amount of alloy to be produced (in lb), $A = \text{alloy\_quant}$
    \item $M$: Number of metals in the alloy
    \item $K$: Number of available alloys
    \item $t_m$: Target quantity of metal $m$, $t_m = \text{target}_m$ for $m = 1, \ldots, M$
    \item $r_{k,m}$: Ratio of metal $m$ in alloy $k$, where $k = 1, \ldots, K$ and $m = 1, \ldots, M$
    \item $p_k$: Price of alloy $k$, where $k = 1, \ldots, K$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_k$: Amount of alloy $k$ to be purchased (in lb), for $k = 1, \ldots, K$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{k=1}^{K} p_k x_k
\]

\textbf{Subject to:}
\begin{align}
    \sum_{k=1}^{K} x_k &= A \quad \text{(Total amount of alloy)} \\
    \sum_{k=1}^{K} r_{k,m} x_k &\geq t_m \quad \text{for } m = 1, \ldots, M \quad \text{(Metal requirements)} \\
    x_k &\geq 0 \quad \text{for } k = 1, \ldots, K \quad \text{(Non-negativity constraint)}
\end{align}

\textbf{Output:}
The solution will provide the quantities of each alloy to purchase:
\[
\text{amount} = [x_1, x_2, \ldots, x_K]
\]

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input Data
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

A = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  #### Number of available alloys
M = len(targets)  #### Number of metals

#### Define the Linear Program
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
problem += pulp.lpSum(x[k] for k in range(K)) == A, "Total_Alloy_Amount"

for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= targets[m], f"Metal_Requirement_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

