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
To create the linear programming model for this problem, we need to define our decision variables, the objective function, and the constraints. Below is the formulation in LaTeX format.

######### Decision Variables
Let \( x_k \) be the amount (in pounds) of alloy \( k \) purchased.

######### Objective Function
Minimize the total cost of purchasing the alloys, given by:
\[ 
\text{Minimize: } \sum_{k=1}^{K} \text{price}_k \cdot x_k 
\]

######### Constraints
1. **Total Weight Constraint**: The total weight of the purchased alloys should equal the required quantity of the final alloy:
   \[
   \sum_{k=1}^{K} x_k = \text{alloy\_quant}
   \]

2. **Metal Composition Constraints**: For each metal \( m \), the weighted average of the ratios from the purchased alloys should match the target ratio in the final alloy:
   \[
   \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant}, \quad \forall m \in \{1, \ldots, M\}
   \]

3. **Non-negativity Constraint**: Each decision variable must be non-negative:
   \[
   x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
   \]

With these components in place, we can write the complete Linear Programming formulation in LaTeX.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model:}

\textbf{Decision Variables:}
\[
x_k \text{ - the amount of alloy } k \text{ purchased (in lb)}
\]

\textbf{Objective:}
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Subject to:}

\begin{enumerate}
    \item Total weight constraint:
    \[
    \sum_{k=1}^{K} x_k = \text{alloy\_quant}
    \]

    \item Metal composition constraints:
    \[
    \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant}, \quad \forall m \in \{1, \ldots, M\}
    \]

    \item Non-negativity:
    \[
    x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
    \]
\end{enumerate}

\end{document}
```

This mathematical model will help the manufacturer find the optimal blend of alloys to minimize cost while meeting the necessary composition and quantity requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model:}

\textbf{Decision Variables:}
\[
x_k \text{ - the amount of alloy } k \text{ purchased (in lb)}
\]

\textbf{Objective:}
\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Subject to:}

\begin{enumerate}
    \item Total weight constraint:
    \[
    \sum_{k=1}^{K} x_k = \text{alloy\_quant}
    \]

    \item Metal composition constraints:
    \[
    \sum_{k=1}^{K} \text{ratio}_{k, m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant}, \quad \forall m \in \{1, \ldots, M\}
    \]

    \item Non-negativity:
    \[
    x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
    \]
\end{enumerate}

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
        [0.95, 0.05],
    ],
    'price': [5, 4, 3, 2, 1.5]
}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  #### Number of alloys
M = len(target)  #### Number of metals

#### Define the Linear Programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum([prices[k] * x[k] for k in range(K)])

#### Constraints
#### Total weight constraint
problem += pulp.lpSum(x) == alloy_quant

#### Metal composition constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) == target[m] * alloy_quant

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

