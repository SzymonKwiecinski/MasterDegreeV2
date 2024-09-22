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
    \item \( alloy\_quant \): Total quantity of the alloy to be produced (in lb).
    \item \( target_{m} \): Target quantity of metal \( m \) (for \( m = 1, \ldots, M \)).
    \item \( ratio_{k, m} \): Ratio of metal \( m \) in alloy \( k \) (for \( k = 1, \ldots, K \) and \( m = 1, \ldots, M \)).
    \item \( price_k \): Price of alloy \( k \) (for \( k = 1, \ldots, K \)).
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item \( amount_k \): Amount of alloy \( k \) to be purchased (for \( k = 1, \ldots, K \)).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} price_k \cdot amount_k
\]

\subsection*{Constraints}
1. Total weight of the alloys must equal the desired alloy weight:
\[
\sum_{k=1}^{K} amount_k = alloy\_quant
\]

2. Each metal \( m \) must meet its target requirement:
\[
\sum_{k=1}^{K} ratio_{k, m} \cdot amount_k = target_{m} \quad \text{for } m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
amount_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Output}
The output should provide the quantities of each alloy to be purchased:
\[
\text{Output: } amount = [amount_k \text{ for } k = 1, \ldots, K]
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
    \item \( alloy\_quant \): Total quantity of the alloy to be produced (in lb).
    \item \( target_{m} \): Target quantity of metal \( m \) (for \( m = 1, \ldots, M \)).
    \item \( ratio_{k, m} \): Ratio of metal \( m \) in alloy \( k \) (for \( k = 1, \ldots, K \) and \( m = 1, \ldots, M \)).
    \item \( price_k \): Price of alloy \( k \) (for \( k = 1, \ldots, K \)).
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item \( amount_k \): Amount of alloy \( k \) to be purchased (for \( k = 1, \ldots, K \)).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} price_k \cdot amount_k
\]

\subsection*{Constraints}
1. Total weight of the alloys must equal the desired alloy weight:
\[
\sum_{k=1}^{K} amount_k = alloy\_quant
\]

2. Each metal \( m \) must meet its target requirement:
\[
\sum_{k=1}^{K} ratio_{k, m} \cdot amount_k = target_{m} \quad \text{for } m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
amount_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Output}
The output should provide the quantities of each alloy to be purchased:
\[
\text{Output: } amount = [amount_k \text{ for } k = 1, \ldots, K]
\]

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [
        [0.1, 0.9],
        [0.25, 0.75],
        [0.5, 0.5],
        [0.75, 0.25],
        [0.95, 0.05]
    ],
    'price': [5, 4, 3, 2, 1.5]
}

#### Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

#### Number of alloys and metals
num_alloys = len(prices)
num_metals = len(target)

#### Problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Variables: amount of each alloy to be purchased
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(num_alloys)]

#### Objective function: Minimize the total cost
problem += pulp.lpSum(prices[k] * amount[k] for k in range(num_alloys))

#### Constraint 1: Total weight of the alloys must equal the desired alloy weight
problem += pulp.lpSum(amount) == alloy_quant

#### Constraint 2: Each metal must meet its target requirement
for m in range(num_metals):
    problem += pulp.lpSum(ratios[k][m] * amount[k] for k in range(num_alloys)) == target[m]

#### Solve the problem
problem.solve()

#### Output the quantities of each alloy to be purchased
amount_values = [pulp.value(amount[k]) for k in range(num_alloys)]
print(f'Quantities to purchase: {amount_values}')

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

