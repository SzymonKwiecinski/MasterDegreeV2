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

A manufacturer wishes to produce \( \text{alloy\_quant} \) lb of an alloy that consists of several kinds of metals. The goal is to meet a target quantity \( \text{target}_{m} \) of metal \( \text{metal}_{m} \). Various alloys are available for purchase, each having different compositions of metals and prices.

\section*{Parameters}

\begin{itemize}
    \item \( \text{alloy\_quant} \): Total weight of the alloy to be produced (in lb).
    \item \( \text{target}_{m} \): Target weight of metal \( \text{metal}_{m} \).
    \item \( \text{ratio}_{k, m} \): Ratio of metal \( \text{metal}_{m} \) in alloy \( k \).
    \item \( \text{price}_{k} \): Selling price of alloy \( k \).
\end{itemize}

\section*{Decision Variables}

Let \( \text{amount}_{k} \) be the amount of alloy \( k \) to purchase (in lb).

\section*{Objective Function}

The manufacturer aims to minimize the total cost of the alloys purchased:

\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_{k} \cdot \text{amount}_{k}
\]

\section*{Constraints}

1. **Alloy Quantity Constraint**:
   The total amount of alloys purchased must equal the required alloy quantity:
   \[
   \sum_{k=1}^{K} \text{amount}_{k} = \text{alloy\_quant}
   \]

2. **Metal Quantity Constraint**:
   The total amount of each metal \( m \) must meet the target quantity:
   \[
   \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot \text{amount}_{k} = \text{target}_{m}, \quad \forall m=1,\ldots,M
   \]

3. **Non-negativity Constraints**:
   \[
   \text{amount}_{k} \geq 0, \quad \forall k=1,\ldots,K
   \]

\section*{Output Information}

The output will be the quantities of each alloy to purchase, represented as:
\[
\text{amount} = [\text{amount}_{k} \text{ for } k = 1, \ldots, K]
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

\title{Linear Programming Model for Alloy Production}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

A manufacturer wishes to produce \( \text{alloy\_quant} \) lb of an alloy that consists of several kinds of metals. The goal is to meet a target quantity \( \text{target}_{m} \) of metal \( \text{metal}_{m} \). Various alloys are available for purchase, each having different compositions of metals and prices.

\section*{Parameters}

\begin{itemize}
    \item \( \text{alloy\_quant} \): Total weight of the alloy to be produced (in lb).
    \item \( \text{target}_{m} \): Target weight of metal \( \text{metal}_{m} \).
    \item \( \text{ratio}_{k, m} \): Ratio of metal \( \text{metal}_{m} \) in alloy \( k \).
    \item \( \text{price}_{k} \): Selling price of alloy \( k \).
\end{itemize}

\section*{Decision Variables}

Let \( \text{amount}_{k} \) be the amount of alloy \( k \) to purchase (in lb).

\section*{Objective Function}

The manufacturer aims to minimize the total cost of the alloys purchased:

\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_{k} \cdot \text{amount}_{k}
\]

\section*{Constraints}

1. **Alloy Quantity Constraint**:
   The total amount of alloys purchased must equal the required alloy quantity:
   \[
   \sum_{k=1}^{K} \text{amount}_{k} = \text{alloy\_quant}
   \]

2. **Metal Quantity Constraint**:
   The total amount of each metal \( m \) must meet the target quantity:
   \[
   \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot \text{amount}_{k} = \text{target}_{m}, \quad \forall m=1,\ldots,M
   \]

3. **Non-negativity Constraints**:
   \[
   \text{amount}_{k} \geq 0, \quad \forall k=1,\ldots,K
   \]

\section*{Output Information}

The output will be the quantities of each alloy to purchase, represented as:
\[
\text{amount} = [\text{amount}_{k} \text{ for } k = 1, \ldots, K]
\]

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

#### Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

#### Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Decision Variables
K = len(price)  #### Number of alloys
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

#### Constraints
#### Alloy Quantity Constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Alloy_Quantity_Constraint"

#### Metal Quantity Constraints
M = len(target)  #### Number of metals
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_Quantity_Constraint_{m+1}"

#### Solve the problem
problem.solve()

#### Output results
amounts = [amount[k].varValue for k in range(K)]
print(f'Amounts: {amounts}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

