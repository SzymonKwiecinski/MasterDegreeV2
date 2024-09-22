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

\section*{Linear Programming Model for Alloy Production}

\textbf{Given:}
\begin{itemize}
    \item \( \text{alloy\_quant} \): Total weight of the alloy to be produced (in lbs).
    \item \( \text{target}_{m} \): Target quantity of metal \( m \) (in lbs).
    \item \( \text{ratio}_{k,m} \): Ratio of metal \( m \) in alloy \( k \).
    \item \( \text{price}_{k} \): Price per lb of alloy \( k \).
\end{itemize}

\textbf{Indices:}
\begin{itemize}
    \item \( k = 1, \ldots, K \): Alloys available for purchase.
    \item \( m = 1, \ldots, M \): Metals in the alloys.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item \( x_k \): Amount of alloy \( k \) to be purchased (in lbs).
\end{itemize}

\textbf{Objective Function:}
Minimize the total cost of the alloys:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_{k} \cdot x_k
\]

\textbf{Constraints:}
\begin{itemize}
    \item Total weight of the alloys must equal the desired alloy weight:
    \[
    \sum_{k=1}^{K} x_k = \text{alloy\_quant}
    \]
    
    \item For each metal \( m \), the total weight of the metal from the alloys must equal the target quantity:
    \[
    \sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_{m}, \quad \forall m \in \{1, \ldots, M\}
    \]
    
    \item Non-negativity constraints on the amounts of alloys:
    \[
    x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
    \]
\end{itemize}

\textbf{Output:}
The solution provides the amounts of each alloy to purchase:
\[
\text{amount} = [x_{1}, x_{2}, \ldots, x_{K}]
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

\section*{Linear Programming Model for Alloy Production}

\textbf{Given:}
\begin{itemize}
    \item \( \text{alloy\_quant} \): Total weight of the alloy to be produced (in lbs).
    \item \( \text{target}_{m} \): Target quantity of metal \( m \) (in lbs).
    \item \( \text{ratio}_{k,m} \): Ratio of metal \( m \) in alloy \( k \).
    \item \( \text{price}_{k} \): Price per lb of alloy \( k \).
\end{itemize}

\textbf{Indices:}
\begin{itemize}
    \item \( k = 1, \ldots, K \): Alloys available for purchase.
    \item \( m = 1, \ldots, M \): Metals in the alloys.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item \( x_k \): Amount of alloy \( k \) to be purchased (in lbs).
\end{itemize}

\textbf{Objective Function:}
Minimize the total cost of the alloys:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_{k} \cdot x_k
\]

\textbf{Constraints:}
\begin{itemize}
    \item Total weight of the alloys must equal the desired alloy weight:
    \[
    \sum_{k=1}^{K} x_k = \text{alloy\_quant}
    \]
    
    \item For each metal \( m \), the total weight of the metal from the alloys must equal the target quantity:
    \[
    \sum_{k=1}^{K} \text{ratio}_{k,m} \cdot x_k = \text{target}_{m}, \quad \forall m \in \{1, \ldots, M\}
    \]
    
    \item Non-negativity constraints on the amounts of alloys:
    \[
    x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
    \]
\end{itemize}

\textbf{Output:}
The solution provides the amounts of each alloy to purchase:
\[
\text{amount} = [x_{1}, x_{2}, \ldots, x_{K}]
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

#### Initialize the problem
problem = pulp.LpProblem("AlloyProduction", pulp.LpMinimize)

#### Variables
num_alloys = len(data['price'])
x = pulp.LpVariable.dicts("Alloy", range(num_alloys), lowBound=0)

#### Objective Function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(num_alloys)])

#### Constraints
#### Total weight constraint
problem += pulp.lpSum([x[k] for k in range(num_alloys)]) == data['alloy_quant']

#### Metal composition constraints
num_metals = len(data['target'])
for m in range(num_metals):
    problem += pulp.lpSum([data['ratio'][k][m] * x[k] for k in range(num_alloys)]) == data['target'][m]

#### Solve the problem
problem.solve()

#### Output the results
solution = [x[k].varValue for k in range(num_alloys)]
print(f'Amounts of each alloy to purchase: {solution}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

