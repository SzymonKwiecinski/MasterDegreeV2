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
To formulate this problem as a Linear Programming (LP) model, let's define the decision variables and constraints based on the given information:

1. **Decision Variables:**
   - Let \( x_k \) be the amount of alloy \( k \) to be purchased for \( k = 1, \ldots, K \).

2. **Objective Function:**
   - Minimize the total cost of purchasing these alloys.
   - The objective function will be:
     \[
     \text{Minimize } \sum_{k=1}^{K} \text{price}_k \times x_k
     \]

3. **Constraints:**
   - **Total Alloy Constraint:** The sum of the alloys purchased should equal the required \( \text{alloy\_quant} \).
     \[
     \sum_{k=1}^{K} x_k = \text{alloy\_quant}
     \]

   - **Metal Composition Constraints:** For each metal \( m = 1, \ldots, M \), the weighted sum of the metal \( m \) content in the purchased alloys should meet the target requirement.
     \[
     \sum_{k=1}^{K} \text{ratio}_{k,m} \times x_k = \text{target}_m \times \text{alloy\_quant}, \quad \forall m = 1, \ldots, M
     \]

The complete LP model in LaTeX is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Alloy Production}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_k \): Amount of alloy \( k \) to be purchased, for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of purchasing alloys:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Total alloy constraint:
    \[
    \sum_{k=1}^{K} x_k = \text{alloy\_quant}
    \]

    \item Metal composition constraints for each metal \( m = 1, \ldots, M \):
    \[
    \sum_{k=1}^{K} \text{ratio}_{k,m} \times x_k = \text{target}_m \times \text{alloy\_quant}, \quad \forall m = 1, \ldots, M
    \]

    \item Non-negativity constraints:
    \[
    x_k \geq 0, \quad \forall k = 1, \ldots, K
    \]
\end{enumerate}

\end{document}
```

This LP model seeks to minimize the cost of the alloys while satisfying both the total alloy quantity and the required metal compositions. The decision variables, objective function, and constraints should be defined in the LP solver using the provided data.

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

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_k \): Amount of alloy \( k \) to be purchased, for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of purchasing alloys:
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \times x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Total alloy constraint:
    \[
    \sum_{k=1}^{K} x_k = \text{alloy\_quant}
    \]

    \item Metal composition constraints for each metal \( m = 1, \ldots, M \):
    \[
    \sum_{k=1}^{K} \text{ratio}_{k,m} \times x_k = \text{target}_m \times \text{alloy\_quant}, \quad \forall m = 1, \ldots, M
    \]

    \item Non-negativity constraints:
    \[
    x_k \geq 0, \quad \forall k = 1, \ldots, K
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
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

#### Extracting data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

#### Number of alloys and metals
K = len(price)
M = len(target)

#### Create the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
#### Total alloy constraint
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Alloy_Constraint"

#### Metal composition constraints
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"Metal_Constraint_{m+1}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

