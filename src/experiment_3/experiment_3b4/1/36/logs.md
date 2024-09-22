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
To solve this problem, we will formulate a linear programming model. This model aims to minimize the cost of purchasing different alloys while meeting the desired alloy composition. We'll use the following notation for the linear program.

Let:
- \( x_k \) be the amount of alloy \( k \) to purchase (for \( k = 1, \ldots, K \)).
- \( \text{alloy\_quant} \) be the total weight of the desired alloy.
- \( \text{target}_m \) be the target proportion of metal \( m \) in the desired alloy (for \( m = 1, \ldots, M \)).
- \( \text{ratio}_{k, m} \) be the proportion of metal \( m \) in alloy \( k \).
- \( \text{price}_k \) be the price of alloy \( k \).

The mathematical model can be expressed as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total cost of purchasing alloys
\[
\min \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Subject to:}
- Total weight constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

- Metal proportion requirements:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant} \quad \text{for each } m = 1, \ldots, M
\]

- Non-negativity constraints:
\[
x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
\]

\end{document}
```

This Linear Programming problem can be solved using tools such as the simplex method or linear programming solvers available in software packages like SciPy, Gurobi, or CPLEX. The solution will provide the optimal amounts \( x_k \) of each alloy \( k \) to purchase to meet the alloy composition at the minimum cost.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total cost of purchasing alloys
\[
\min \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Subject to:}
- Total weight constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

- Metal proportion requirements:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant} \quad \text{for each } m = 1, \ldots, M
\]

- Non-negativity constraints:
\[
x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
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

alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
K = len(price)
M = len(target)

#### Problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

#### Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

#### Objective
problem += pulp.lpSum(price[k] * x[k] for k in range(K))

#### Total weight constraint
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant

#### Metal proportion requirements
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m] * alloy_quant

#### Solve
problem.solve()

#### Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

