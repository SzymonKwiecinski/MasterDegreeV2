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
To solve this problem, we will set up a linear programming model. Our objective is to minimize the cost of purchasing various alloys while ensuring that the resulting alloy meets the target composition requirements. Here is the mathematical model of the given problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Alloy Production}

\subsection*{Parameters:}
\begin{itemize}
    \item $alloy\_quant$: Total quantity of the alloy to be produced.
    \item $M$: Number of metals in the target alloy composition.
    \item $K$: Number of available alloys.
    \item $target_m$: Target weight of metal $m$ in the desired alloy.
    \item $ratio_{k,m}$: Ratio of metal $m$ in alloy $k$.
    \item $price_k$: Price of alloy $k$.
\end{itemize}

\subsection*{Decision Variables:}
\begin{itemize}
    \item $amount_k$: Quantity of alloy $k$ to purchase.
\end{itemize}

\subsection*{Objective Function:}

Minimize the total cost of purchasing the alloys:
\[
\text{Minimize } \sum_{k=1}^{K} price_k \times amount_k
\]

\subsection*{Constraints:}

1. Total weight constraint:
   \[
   \sum_{k=1}^{K} amount_k = alloy\_quant
   \]

2. Metal composition constraints for each metal $m$, where $m=1,...,M$:
   \[
   \sum_{k=1}^{K} ratio_{k,m} \times amount_k \geq target_m
   \]

3. Non-negativity constraints:
   \[
   amount_k \geq 0 \quad \text{for } k=1,...,K
   \]

\subsection*{Conclusion:}

The solution to this linear programming problem will provide the optimal quantities of each alloy to purchase in order to achieve the desired alloy composition at the minimum cost.

\end{document}
```

This model captures the problem of selecting the optimal combination of available alloys to meet the target alloy specifications at the lowest possible cost. Constraints ensure both the total alloy weight and the composition of each metal are met, and the decision variable $amount_k$ denotes the quantity of each alloy to be used.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Alloy Production}

\subsection*{Parameters:}
\begin{itemize}
    \item $alloy\_quant$: Total quantity of the alloy to be produced.
    \item $M$: Number of metals in the target alloy composition.
    \item $K$: Number of available alloys.
    \item $target_m$: Target weight of metal $m$ in the desired alloy.
    \item $ratio_{k,m}$: Ratio of metal $m$ in alloy $k$.
    \item $price_k$: Price of alloy $k$.
\end{itemize}

\subsection*{Decision Variables:}
\begin{itemize}
    \item $amount_k$: Quantity of alloy $k$ to purchase.
\end{itemize}

\subsection*{Objective Function:}

Minimize the total cost of purchasing the alloys:
\[
\text{Minimize } \sum_{k=1}^{K} price_k \times amount_k
\]

\subsection*{Constraints:}

1. Total weight constraint:
   \[
   \sum_{k=1}^{K} amount_k = alloy\_quant
   \]

2. Metal composition constraints for each metal $m$, where $m=1,...,M$:
   \[
   \sum_{k=1}^{K} ratio_{k,m} \times amount_k \geq target_m
   \]

3. Non-negativity constraints:
   \[
   amount_k \geq 0 \quad \text{for } k=1,...,K
   \]

\subsection*{Conclusion:}

The solution to this linear programming problem will provide the optimal quantities of each alloy to purchase in order to achieve the desired alloy composition at the minimum cost.

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format.
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  #### Number of available alloys
M = len(target)  #### Number of metals in the target alloy composition

#### Create the linear programming problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

#### Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

#### Total weight constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Weight"

#### Metal composition constraints
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) >= target[m], f"Composition_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

