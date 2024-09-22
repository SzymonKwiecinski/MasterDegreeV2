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
To formulate this problem as a linear programming model, we need to determine the amounts of different alloys to buy in order to meet the required composition of the target alloy at the minimum cost. Below is a linear programming formulation for this problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Given:}
\begin{itemize}
    \item Total quantity of alloy required: \( \text{alloy\_quant} \)
    \item Target composition of each metal \( m \) in the alloy: \(\text{target}_m\), for \( m = 1, \ldots, M \)
    \item Composition ratio of metal \( m \) in alloy \( k \): \(\text{ratio}_{k, m}\)
    \item Cost of each available alloy \( k \): \(\text{price}_k\)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( \text{amount}_k \) be the amount of alloy \( k \) purchased, for \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Objective:}
Minimize the total cost of purchasing the alloys:
\[
\text{Minimize } \sum_{k=1}^{K} \text{price}_k \cdot \text{amount}_k
\]

\textbf{Subject to:}
\begin{itemize}
    \item Total weight constraint:
    \[
    \sum_{k=1}^{K} \text{amount}_k = \text{alloy\_quant}
    \]
    \item Composition constraints for each metal \( m \):
    \[
    \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot \text{amount}_k = \text{target}_m \times \text{alloy\_quant}, \quad \forall m = 1, \ldots, M
    \]
    \item Non-negativity constraints:
    \[
    \text{amount}_k \geq 0, \quad \forall k = 1, \ldots, K
    \]
\end{itemize}

This linear program can be solved using appropriate LP solvers to find the optimal amounts of each type of alloy to purchase.

\end{document}
```

This formulation will help determine the cheapest combination of alloys needed to produce the required amount of the target alloy. The constraints ensure that the total weight and target composition conditions are satisfied.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Given:}
\begin{itemize}
    \item Total quantity of alloy required: \( \text{alloy\_quant} \)
    \item Target composition of each metal \( m \) in the alloy: \(\text{target}_m\), for \( m = 1, \ldots, M \)
    \item Composition ratio of metal \( m \) in alloy \( k \): \(\text{ratio}_{k, m}\)
    \item Cost of each available alloy \( k \): \(\text{price}_k\)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( \text{amount}_k \) be the amount of alloy \( k \) purchased, for \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Objective:}
Minimize the total cost of purchasing the alloys:
\[
\text{Minimize } \sum_{k=1}^{K} \text{price}_k \cdot \text{amount}_k
\]

\textbf{Subject to:}
\begin{itemize}
    \item Total weight constraint:
    \[
    \sum_{k=1}^{K} \text{amount}_k = \text{alloy\_quant}
    \]
    \item Composition constraints for each metal \( m \):
    \[
    \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot \text{amount}_k = \text{target}_m \times \text{alloy\_quant}, \quad \forall m = 1, \ldots, M
    \]
    \item Non-negativity constraints:
    \[
    \text{amount}_k \geq 0, \quad \forall k = 1, \ldots, K
    \]
\end{itemize}

This linear program can be solved using appropriate LP solvers to find the optimal amounts of each type of alloy to purchase.

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Problem data
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

#### Initialize the LP problem
problem = pulp.LpProblem("Alloy_Mixture_Problem", pulp.LpMinimize)

#### Number of alloys and metals
K = len(data['price'])  #### number of different alloys
M = len(data['target'])  #### number of metals

#### Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function: Minimize the total cost of purchasing the alloys
problem += pulp.lpSum(data['price'][k] * amount[k] for k in range(K))

#### Constraints
#### Total weight constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == data['alloy_quant']

#### Composition constraints for each metal
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * amount[k] for k in range(K)) == data['target'][m]

#### Solve the problem
problem.solve()

#### Print the objective value (total cost)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

