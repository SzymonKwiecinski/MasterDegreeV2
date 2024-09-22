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
To formulate the given problem as a linear programming model, we will define the decision variables, objective function, and constraints using LaTeX.

######### Decision Variables:
- \( x_k \): The amount (in pounds) of alloy \( k \) purchased, for \( k = 1, 2, \ldots, K \).

######### Objective Function:
- Minimize the total cost of the alloys purchased.

######### Constraints:
1. The total quantity of the alloy produced should be equal to \( \text{alloy\_quant} \).
2. The proportion of each metal \( m \) in the final alloy should meet the target specification.

Now, let's write the model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} \text{price}_k \cdot x_k \\
\text{subject to} \quad & \sum_{k=1}^{K} x_k = \text{alloy\_quant}, \\
& \sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant}, \quad \forall m = 1, 2, \ldots, M, \\
& x_k \geq 0, \quad \forall k = 1, 2, \ldots, K.
\end{align*}

\end{document}
```

Here, we've defined:
- An objective function to minimize the total cost of purchasing the desired alloys.
- A constraint ensuring the total weight of the produced alloy is equal to \(\text{alloy\_quant}\).
- Additional constraints ensuring each metal's proportion meets the specified target.
- Non-negativity constraints for the decision variables \(x_k\). 

This model can then be solved using any linear programming solver to find the optimal amounts for each alloy.

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

\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} \text{price}_k \cdot x_k \\
\text{subject to} \quad & \sum_{k=1}^{K} x_k = \text{alloy\_quant}, \\
& \sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_m \cdot \text{alloy\_quant}, \quad \forall m = 1, 2, \ldots, M, \\
& x_k \geq 0, \quad \forall k = 1, 2, \ldots, K.
\end{align*}

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
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

#### Problem Definition
problem = pulp.LpProblem("Alloy_Mixture_Minimization", pulp.LpMinimize)

#### Decision Variables
K = len(data['price'])
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

#### Objective Function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)])

#### Constraints
#### Total Alloy Quantity Constraint
problem += pulp.lpSum(x) == data['alloy_quant']

#### Target Content Constraints
M = len(data['target'])
for m in range(M):
    problem += pulp.lpSum([data['ratio'][k][m] * x[k] for k in range(K)]) == data['target'][m] * data['alloy_quant']

#### Solve
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

