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

\title{Linear Programming Model for Alloy Production}
\author{}
\date{}
\maketitle

\section*{Problem Definition}
A manufacturer wishes to produce \( \text{alloy\_quant} \) lb of an alloy that consists of several kinds of metals. The target quantity of metal \( m \) in the alloy is given by \( \text{target}_{m} \). The available alloys \( k \) have a ratio \( \text{ratio}_{k, m} \) of metal \( m \) and are sold at a price \( \text{price}_{k} \).

\section*{Decision Variables}
Let \( \text{amount}_{k} \) be the quantity of alloy \( k \) to be purchased.

\section*{Objective Function}
The objective is to minimize the total cost of the alloys purchased:

\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_{k} \cdot \text{amount}_{k}
\]

\section*{Constraints}

1. Total weight of the alloys must equal the desired alloy weight:

\[
\sum_{k=1}^{K} \text{amount}_{k} = \text{alloy\_quant}
\]

2. Ensure that the weight of metal \( m \) meets the target:

\[
\sum_{k=1}^{K} \text{ratio}_{k, m} \cdot \text{amount}_{k} = \text{target}_{m}, \quad \text{for } m = 1, \ldots, M
\]

3. Non-negativity constraints:

\[
\text{amount}_{k} \geq 0, \quad \text{for } k = 1, \ldots, K
\]

\section*{Summary of Input and Output}

\textbf{Input:}
\begin{itemize}
    \item \text{alloy\_quant} - Total quantity of the alloy to be produced.
    \item \text{target} - Target quantities of metals in the alloy \(\text{target}_{m}\) for \( m = 1, \ldots, M \).
    \item \text{ratio} - Ratios of metals in each alloy \(\text{ratio}_{k, m}\) for \( k = 1, \ldots, K \) and \( m = 1, \ldots, M \).
    \item \text{price} - Prices of each alloy \(\text{price}_{k}\) for \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item \text{amount} - Quantities of each alloy to be purchased \(\text{amount}_{k}\) for \( k = 1, \ldots, K \).
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

\title{Linear Programming Model for Alloy Production}
\author{}
\date{}
\maketitle

\section*{Problem Definition}
A manufacturer wishes to produce \( \text{alloy\_quant} \) lb of an alloy that consists of several kinds of metals. The target quantity of metal \( m \) in the alloy is given by \( \text{target}_{m} \). The available alloys \( k \) have a ratio \( \text{ratio}_{k, m} \) of metal \( m \) and are sold at a price \( \text{price}_{k} \).

\section*{Decision Variables}
Let \( \text{amount}_{k} \) be the quantity of alloy \( k \) to be purchased.

\section*{Objective Function}
The objective is to minimize the total cost of the alloys purchased:

\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_{k} \cdot \text{amount}_{k}
\]

\section*{Constraints}

1. Total weight of the alloys must equal the desired alloy weight:

\[
\sum_{k=1}^{K} \text{amount}_{k} = \text{alloy\_quant}
\]

2. Ensure that the weight of metal \( m \) meets the target:

\[
\sum_{k=1}^{K} \text{ratio}_{k, m} \cdot \text{amount}_{k} = \text{target}_{m}, \quad \text{for } m = 1, \ldots, M
\]

3. Non-negativity constraints:

\[
\text{amount}_{k} \geq 0, \quad \text{for } k = 1, \ldots, K
\]

\section*{Summary of Input and Output}

\textbf{Input:}
\begin{itemize}
    \item \text{alloy\_quant} - Total quantity of the alloy to be produced.
    \item \text{target} - Target quantities of metals in the alloy \(\text{target}_{m}\) for \( m = 1, \ldots, M \).
    \item \text{ratio} - Ratios of metals in each alloy \(\text{ratio}_{k, m}\) for \( k = 1, \ldots, K \) and \( m = 1, \ldots, M \).
    \item \text{price} - Prices of each alloy \(\text{price}_{k}\) for \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item \text{amount} - Quantities of each alloy to be purchased \(\text{amount}_{k}\) for \( k = 1, \ldots, K \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

#### Problem parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  #### number of alloys
M = len(target)  #### number of metals

#### Creating the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total Cost"

#### Constraints
#### Total weight must equal the desired alloy weight
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total Alloys Weight"

#### Constraints for each metal
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_{m+1}_Requirement"

#### Solve the problem
problem.solve()

#### Output the results
amount_values = {k: amount[k].varValue for k in range(K)}
print(f'Amount of each alloy to purchase: {amount_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

