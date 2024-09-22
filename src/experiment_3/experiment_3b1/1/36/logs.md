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

\subsection*{Parameters}
\begin{itemize}
    \item Let \( A \) be the total quantity of the alloy to be produced: \( A = \text{alloy\_quant} \)
    \item Let \( M \) be the number of metals: \( M = \text{len(target)} \)
    \item Let \( K \) be the number of available alloys: \( K = \text{len(price)} \)
    \item Let \( t_m \) be the target quantity of metal \( m \): \( t_m = \text{target}[m], \; m = 1, \ldots, M \)
    \item Let \( r_{k, m} \) be the ratio of metal \( m \) in alloy \( k \): \( r_{k, m} = \text{ratio}[k][m], \; k = 1, \ldots, K, \; m = 1, \ldots, M \)
    \item Let \( p_k \) be the price of alloy \( k \): \( p_k = \text{price}[k], \; k = 1, \ldots, K \)
    \item Let \( x_k \) be the amount of alloy \( k \) to be purchased: \( x_k = \text{amount}[k], \; k = 1, \ldots, K \)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of alloys purchased:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} p_k x_k
\]

\subsection*{Constraints}
1. The total weight of the alloys must equal \( A \):
\[
\sum_{k=1}^{K} x_k = A
\]

2. The amount of each metal \( m \) in the alloys must meet the target requirement:
\[
\sum_{k=1}^{K} r_{k, m} x_k = t_m, \quad m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0, \quad k = 1, \ldots, K
\]

\subsection*{Output}
The output will be the amounts of each alloy to be purchased:
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

\section*{Linear Programming Model for Alloy Production}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( A \) be the total quantity of the alloy to be produced: \( A = \text{alloy\_quant} \)
    \item Let \( M \) be the number of metals: \( M = \text{len(target)} \)
    \item Let \( K \) be the number of available alloys: \( K = \text{len(price)} \)
    \item Let \( t_m \) be the target quantity of metal \( m \): \( t_m = \text{target}[m], \; m = 1, \ldots, M \)
    \item Let \( r_{k, m} \) be the ratio of metal \( m \) in alloy \( k \): \( r_{k, m} = \text{ratio}[k][m], \; k = 1, \ldots, K, \; m = 1, \ldots, M \)
    \item Let \( p_k \) be the price of alloy \( k \): \( p_k = \text{price}[k], \; k = 1, \ldots, K \)
    \item Let \( x_k \) be the amount of alloy \( k \) to be purchased: \( x_k = \text{amount}[k], \; k = 1, \ldots, K \)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of alloys purchased:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} p_k x_k
\]

\subsection*{Constraints}
1. The total weight of the alloys must equal \( A \):
\[
\sum_{k=1}^{K} x_k = A
\]

2. The amount of each metal \( m \) in the alloys must meet the target requirement:
\[
\sum_{k=1}^{K} r_{k, m} x_k = t_m, \quad m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0, \quad k = 1, \ldots, K
\]

\subsection*{Output}
The output will be the amounts of each alloy to be purchased:
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
import json

#### Input data
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

#### Parameters
A = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

M = len(target)  #### Number of metals
K = len(price)   #### Number of available alloys

#### Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Define decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraint 1: Total weight of the alloys
problem += pulp.lpSum(x[k] for k in range(K)) == A, "Total_Weight"

#### Constraints for each metal to meet the target
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"Metal_Requirement_{m+1}"

#### Solve the problem
problem.solve()

#### Output the amounts of each alloy to be purchased
amounts = [x[k].varValue for k in range(K)]

print(f'Amounts of each alloy to be purchased: {amounts}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

