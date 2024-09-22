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

\textbf{Variables:}
\begin{itemize}
    \item Let \( a_k \) represent the amount of alloy \( k \) to be purchased (in lb), for \( k = 1, 2, \ldots, K \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{alloy\_quant} \): Total quantity of alloy to be produced (in lb).
    \item \( \text{target}_m \): Target quantity of metal \( m \) in the final alloy (in lb), for \( m = 1, 2, \ldots, M \).
    \item \( \text{ratio}_{k,m} \): Ratio of metal \( m \) in alloy \( k \).
    \item \( \text{price}_k \): Price per lb of alloy \( k \).
\end{itemize}

\textbf{Objective:} Minimize the total cost of the alloys used.
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot a_k
\]

\textbf{Constraints:}
1. The total weight of the alloys used must equal the target alloy weight:
\[
\sum_{k=1}^{K} a_k = \text{alloy\_quant}
\]

2. The total amount of each metal \( m \) must meet the target:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot a_k = \text{target}_m, \quad \text{for } m = 1, 2, \ldots, M
\]

3. Non-negativity constraints:
\[
a_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\]

\textbf{Output Variables:}
The output will consist of the amounts of each alloy purchased:
\[
\text{amount} = [a_k \text{ for } k = 1, \ldots, K]
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

\section*{Linear Programming Model for Alloy Production}

\textbf{Variables:}
\begin{itemize}
    \item Let \( a_k \) represent the amount of alloy \( k \) to be purchased (in lb), for \( k = 1, 2, \ldots, K \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{alloy\_quant} \): Total quantity of alloy to be produced (in lb).
    \item \( \text{target}_m \): Target quantity of metal \( m \) in the final alloy (in lb), for \( m = 1, 2, \ldots, M \).
    \item \( \text{ratio}_{k,m} \): Ratio of metal \( m \) in alloy \( k \).
    \item \( \text{price}_k \): Price per lb of alloy \( k \).
\end{itemize}

\textbf{Objective:} Minimize the total cost of the alloys used.
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot a_k
\]

\textbf{Constraints:}
1. The total weight of the alloys used must equal the target alloy weight:
\[
\sum_{k=1}^{K} a_k = \text{alloy\_quant}
\]

2. The total amount of each metal \( m \) must meet the target:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot a_k = \text{target}_m, \quad \text{for } m = 1, 2, \ldots, M
\]

3. Non-negativity constraints:
\[
a_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\]

\textbf{Output Variables:}
The output will consist of the amounts of each alloy purchased:
\[
\text{amount} = [a_k \text{ for } k = 1, \ldots, K]
\]

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

#### Number of alloys and metals
K = len(data['price'])  #### Number of alloys
M = len(data['target'])  #### Number of metals

#### Create the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Decision variables
a = [pulp.LpVariable(f'a_{k}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(data['price'][k] * a[k] for k in range(K)), "Total Cost"

#### Constraint 1: The total weight of the alloys used must equal the target alloy weight
problem += pulp.lpSum(a[k] for k in range(K)) == data['alloy_quant'], "Total Alloy Quantity"

#### Constraint 2: The total amount of each metal m must meet the target
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * a[k] for k in range(K)) == data['target'][m], f"Metal_{m}_Target"

#### Solve the problem
problem.solve()

#### Output the results
amounts = [pulp.value(a_k) for a_k in a]
print("Amounts purchased for each alloy:", amounts)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

