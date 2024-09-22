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
    \item Let \( alloy\_quant \) be the total weight of the alloy to be produced (in lb).
    \item Let \( target_m \) be the target quantity of metal \( m \) in the alloy (for \( m=1, \ldots, M \)).
    \item Let \( ratio_{k, m} \) be the ratio of metal \( m \) in alloy \( k \) (for \( k=1, \ldots, K \) and \( m=1, \ldots, M \)).
    \item Let \( price_k \) be the price of alloy \( k \).
\end{itemize}

\subsection*{Decision Variables}

Let \( amount_k \) represent the quantity of alloy \( k \) that we buy (for \( k=1, \ldots, K \)).

\subsection*{Objective Function}

The objective is to minimize the total cost of the alloys used:

\[
\text{Minimize } Z = \sum_{k=1}^{K} price_k \cdot amount_k
\]

\subsection*{Constraints}

1. The total weight of the alloys used must equal the desired weight of the alloy:
\[
\sum_{k=1}^{K} amount_k = alloy\_quant
\]

2. For each metal \( m \), the total amount of that metal contributed by the alloys must equal the desired target quantity:
\[
\sum_{k=1}^{K} ratio_{k, m} \cdot amount_k = target_m \quad \text{for } m = 1, 2, \ldots, M
\]

3. Non-negativity constraints:
\[
amount_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
\]

\subsection*{Output}

The output will be the amounts of each alloy to purchase:

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
    \item Let \( alloy\_quant \) be the total weight of the alloy to be produced (in lb).
    \item Let \( target_m \) be the target quantity of metal \( m \) in the alloy (for \( m=1, \ldots, M \)).
    \item Let \( ratio_{k, m} \) be the ratio of metal \( m \) in alloy \( k \) (for \( k=1, \ldots, K \) and \( m=1, \ldots, M \)).
    \item Let \( price_k \) be the price of alloy \( k \).
\end{itemize}

\subsection*{Decision Variables}

Let \( amount_k \) represent the quantity of alloy \( k \) that we buy (for \( k=1, \ldots, K \)).

\subsection*{Objective Function}

The objective is to minimize the total cost of the alloys used:

\[
\text{Minimize } Z = \sum_{k=1}^{K} price_k \cdot amount_k
\]

\subsection*{Constraints}

1. The total weight of the alloys used must equal the desired weight of the alloy:
\[
\sum_{k=1}^{K} amount_k = alloy\_quant
\]

2. For each metal \( m \), the total amount of that metal contributed by the alloys must equal the desired target quantity:
\[
\sum_{k=1}^{K} ratio_{k, m} \cdot amount_k = target_m \quad \text{for } m = 1, 2, \ldots, M
\]

3. Non-negativity constraints:
\[
amount_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
\]

\subsection*{Output}

The output will be the amounts of each alloy to purchase:

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

#### Data from JSON
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
targets = data['target']
ratios = data['ratio']
prices = data['price']
K = len(prices)
M = len(targets)

#### Linear Programming problem
problem = pulp.LpProblem("Alloy_Production_Cost_Minimization", pulp.LpMinimize)

#### Decision Variables
amounts = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

#### Objective Function
problem += pulp.lpSum(prices[k] * amounts[k] for k in range(K)), "Total Cost"

#### Constraints
#### Total weight constraint
problem += pulp.lpSum(amounts[k] for k in range(K)) == alloy_quant, "Total_Weight_Constraint"

#### Metal target constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * amounts[k] for k in range(K)) == targets[m], f"Metal_{m+1}_Target_Constraint"

#### Solve the problem
problem.solve()

#### Output the results
amount = [pulp.value(amounts[k]) for k in range(K)]
print(f'Amounts of each alloy to purchase: {amount}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

