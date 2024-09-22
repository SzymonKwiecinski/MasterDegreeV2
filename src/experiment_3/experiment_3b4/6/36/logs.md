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
To solve this linear programming problem, we need to determine the amounts of the various alloys to purchase to meet the target composition at the minimum cost. Let's construct the mathematical model as follows:

Objective: Minimize the total cost of purchasing the alloys.

Constraints:
1. The sum of the amounts of all alloys must be equal to the desired alloy quantity.
2. For each metal \( m \), the weighted sum of the metal ratios from the chosen alloys must meet the target composition.

Let us denote:
- \( x_k \) as the amount of alloy \( k \) purchased.
- \( a_k \) as the price of alloy \( k \).
- \( r_{k,m} \) as the ratio of metal \( m \) in alloy \( k \).
- \( t_m \) as the target weight of metal \( m \) in the alloy.
- \( A \) as the total amount of alloy needed.

The linear programming model in LaTeX will be:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Minimize the cost:
\begin{equation}
\text{Minimize } \sum_{k=1}^K a_k x_k
\end{equation}

\subsection*{Constraints}
1. Total alloy constraint:
\begin{equation}
\sum_{k=1}^K x_k = A
\end{equation}

2. Metal composition constraints:
\begin{equation}
\sum_{k=1}^K r_{k,m} x_k = t_m \cdot A \quad \text{for each } m \in \{1, 2, \ldots, M\}
\end{equation}

\subsection*{Non-negativity}
\begin{equation}
x_k \geq 0 \quad \text{for all } k \in \{1, 2, \ldots, K\}
\end{equation}

\end{document}
```

Here, the constraints ensure that the total weight of all alloys equals the desired amount, and the target composition is met for each metal. The non-negativity constraint ensures that the quantities purchased are not negative.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Minimize the cost:
\begin{equation}
\text{Minimize } \sum_{k=1}^K a_k x_k
\end{equation}

\subsection*{Constraints}
1. Total alloy constraint:
\begin{equation}
\sum_{k=1}^K x_k = A
\end{equation}

2. Metal composition constraints:
\begin{equation}
\sum_{k=1}^K r_{k,m} x_k = t_m \cdot A \quad \text{for each } m \in \{1, 2, \ldots, M\}
\end{equation}

\subsection*{Non-negativity}
\begin{equation}
x_k \geq 0 \quad \text{for all } k \in \{1, 2, \ldots, K\}
\end{equation}

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

#### Define the problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

#### Decision variables
K = len(data['price'])
x = [pulp.LpVariable(f'x{k+1}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)])

#### Total alloy constraint
problem += pulp.lpSum(x) == data['alloy_quant']

#### Metal composition constraints
for m in range(len(data['target'])):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(K)) == data['target'][m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

