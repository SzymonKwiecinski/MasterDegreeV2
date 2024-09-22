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

\section*{Problem Formulation}

Let:
\begin{itemize}
    \item \( A \) be the total amount of alloy required (\( \text{alloy\_quant} \)).
    \item \( T_m \) be the target quantity of metal \( m \) (\( \text{target}_{m} \)).
    \item \( R_{k,m} \) be the ratio of metal \( m \) in alloy \( k \) (\( \text{ratio}_{k, m} \)).
    \item \( P_k \) be the price of alloy \( k \) (\( \text{price}_{k} \)).
    \item \( x_k \) be the amount of alloy \( k \) to purchase.
\end{itemize}

\section*{Objective Function}

The objective is to minimize the total cost of the alloys purchased:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} P_k \cdot x_k
\]

\section*{Constraints}

1. The total weight of all alloys must equal the desired amount of the alloy:
\[
\sum_{k=1}^{K} x_k = A
\]

2. The total amount of each metal \( m \) in the alloys must meet the target quantity:
\[
\sum_{k=1}^{K} R_{k,m} \cdot x_k = T_m \quad \forall m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\section*{Solution Variables}

The solution variable represents the amounts of each alloy to purchase:
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

\title{Linear Programming Model for Alloy Production}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

Let:
\begin{itemize}
    \item \( A \) be the total amount of alloy required (\( \text{alloy\_quant} \)).
    \item \( T_m \) be the target quantity of metal \( m \) (\( \text{target}_{m} \)).
    \item \( R_{k,m} \) be the ratio of metal \( m \) in alloy \( k \) (\( \text{ratio}_{k, m} \)).
    \item \( P_k \) be the price of alloy \( k \) (\( \text{price}_{k} \)).
    \item \( x_k \) be the amount of alloy \( k \) to purchase.
\end{itemize}

\section*{Objective Function}

The objective is to minimize the total cost of the alloys purchased:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} P_k \cdot x_k
\]

\section*{Constraints}

1. The total weight of all alloys must equal the desired amount of the alloy:
\[
\sum_{k=1}^{K} x_k = A
\]

2. The total amount of each metal \( m \) in the alloys must meet the target quantity:
\[
\sum_{k=1}^{K} R_{k,m} \cdot x_k = T_m \quad \forall m = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\section*{Solution Variables}

The solution variable represents the amounts of each alloy to purchase:
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

#### Data input
data_json = '''{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}'''
data = json.loads(data_json)

#### Problem parameters
A = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']
K = len(prices)
M = len(targets)

#### Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K))

#### Constraints
#### Total weight of alloys equals A
problem += pulp.lpSum(x[k] for k in range(K)) == A

#### Each metal's target quantity constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) == targets[m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

