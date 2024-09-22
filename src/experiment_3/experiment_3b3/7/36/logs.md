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
	\item $A$ = total weight of the alloy to be produced (in lb) = \texttt{alloy\_quant}
	\item $M$ = number of metals
	\item $K$ = number of available alloys
	\item $t_m$ = target quantity of metal $m$ = \texttt{target}[m] for $m = 1, \ldots, M$
	\item $r_{k,m}$ = ratio of metal $m$ in alloy $k$ = \texttt{ratio}[k][m] for $k = 1, \ldots, K$ and $m = 1, \ldots, M$
	\item $p_k$ = price of alloy $k$ = \texttt{price}[k] for $k = 1, \ldots, K$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
	\item $x_k$ = amount of alloy $k$ to purchase (in lb) for $k = 1, \ldots, K$
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Minimize } Z = \sum_{k=1}^{K} p_k x_k
\end{align*}

\textbf{Subject to the Constraints:}

\begin{align}
\sum_{k=1}^{K} x_k = A \quad & \text{(Total amount of alloys produced)} \tag{1} \\
\sum_{k=1}^{K} r_{k,m} x_k = t_m \quad & \text{for } m = 1, \ldots, M \quad \text{(Metal composition requirement)} \tag{2} \\
x_k \geq 0 \quad & \text{for } k = 1, \ldots, K \quad \text{(Non-negativity)} \tag{3}
\end{align}

\textbf{Output:}
The solution will provide the amounts of each alloy to purchase:
\begin{align*}
\text{amount} = [x_k \text{ for } k = 1, \ldots, K]
\end{align*}

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
	\item $A$ = total weight of the alloy to be produced (in lb) = \texttt{alloy\_quant}
	\item $M$ = number of metals
	\item $K$ = number of available alloys
	\item $t_m$ = target quantity of metal $m$ = \texttt{target}[m] for $m = 1, \ldots, M$
	\item $r_{k,m}$ = ratio of metal $m$ in alloy $k$ = \texttt{ratio}[k][m] for $k = 1, \ldots, K$ and $m = 1, \ldots, M$
	\item $p_k$ = price of alloy $k$ = \texttt{price}[k] for $k = 1, \ldots, K$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
	\item $x_k$ = amount of alloy $k$ to purchase (in lb) for $k = 1, \ldots, K$
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Minimize } Z = \sum_{k=1}^{K} p_k x_k
\end{align*}

\textbf{Subject to the Constraints:}

\begin{align}
\sum_{k=1}^{K} x_k = A \quad & \text{(Total amount of alloys produced)} \tag{1} \\
\sum_{k=1}^{K} r_{k,m} x_k = t_m \quad & \text{for } m = 1, \ldots, M \quad \text{(Metal composition requirement)} \tag{2} \\
x_k \geq 0 \quad & \text{for } k = 1, \ldots, K \quad \text{(Non-negativity)} \tag{3}
\end{align}

\textbf{Output:}
The solution will provide the amounts of each alloy to purchase:
\begin{align*}
\text{amount} = [x_k \text{ for } k = 1, \ldots, K]
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

#### Extract parameters
A = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
M = len(target)
K = len(price)

#### Initialize the LP problem
problem = pulp.LpProblem("Alloy_Production_Minimize_Cost", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K))

#### Constraint: Total amount of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == A, "Total_Alloy_Quantity"

#### Constraints: Metal composition requirements
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"Metal_Composition_{m+1}"

#### Solve the problem
problem.solve()

#### Output results
amounts = {f'x_{k}': pulp.value(x[k]) for k in range(K)}
print("The amounts of each alloy to purchase:")
for k in amounts:
    print(f'{k}: {amounts[k]}')

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

