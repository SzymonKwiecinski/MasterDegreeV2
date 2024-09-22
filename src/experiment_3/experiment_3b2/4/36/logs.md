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
To create a linear programming model for this problem, we'll define decision variables, objective function, and constraints based on the given information. Let's define the decision variables as \(x_k\), representing the amount of each alloy \(k\) that we need to buy.

Objective: Minimize the total cost of purchasing the alloys.

Constraints: 
1. The total weight of the mixed alloys should be equal to the desired alloy quantity.
2. Each metal \(m\) should meet the target ratio in the final alloy.

Let's form the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Given:}
\begin{itemize}
    \item Desired total alloy quantity: \( \text{alloy\_quant} \)
    \item Target ratios for metals: \( \text{target}_m \) for each metal \( m \)
    \item Composition ratio of each metal in each alloy: \( \text{ratio}_{k,m} \)
    \item Price of each alloy: \( \text{price}_k \)
\end{itemize}

\textbf{Decision Variables:}
\[
x_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]
where \( x_k \) is the quantity of alloy \( k \) to be purchased.

\textbf{Objective Function:}
\[
\text{Minimize } \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Constraints:}
1. Total alloy weight constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal composition constraints:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{alloy\_quant} \cdot \text{target}_m \quad \text{for } m = 1, \ldots, M
\]

\end{document}
```

This model will allow you to compute the optimal amounts of each alloy to purchase in order to minimize cost while meeting the weight and composition requirements.

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

\textbf{Given:}
\begin{itemize}
    \item Desired total alloy quantity: \( \text{alloy\_quant} \)
    \item Target ratios for metals: \( \text{target}_m \) for each metal \( m \)
    \item Composition ratio of each metal in each alloy: \( \text{ratio}_{k,m} \)
    \item Price of each alloy: \( \text{price}_k \)
\end{itemize}

\textbf{Decision Variables:}
\[
x_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]
where \( x_k \) is the quantity of alloy \( k \) to be purchased.

\textbf{Objective Function:}
\[
\text{Minimize } \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\textbf{Constraints:}
1. Total alloy weight constraint:
\[
\sum_{k=1}^{K} x_k = \text{alloy\_quant}
\]

2. Metal composition constraints:
\[
\sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{alloy\_quant} \cdot \text{target}_m \quad \text{for } m = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data as a JSON string
data = '''{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}'''
data = json.loads(data.replace("'", "\""))  #### Convert to proper JSON format

#### Extract data
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

#### Number of alloys and metals
K = len(price)
M = len(target)

#### Create the optimization problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("Alloy_Quantity", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Alloy_Weight"

for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == alloy_quant * target[m], f"Metal_Composition_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

