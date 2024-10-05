# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A mining company is going to continue operating in a certain area for the next years. 
- There are \var{n_mines} mines in this area, but it can operate at most \var{n_maxwork} in any one year. 
- Although a mine may not operate in a certain year, it is still necessary to keep it ‘open’, in the sense that royalties are payable, if it be operated in a future year. 
- Clearly, if a mine is not going to be worked again, it can be permanently closed down and no more royalties need be paid. 
- The yearly royalties payable on each mine kept ‘open’ is \var{royalty_{k}} for mine \var{k}.
- There is an upper limit to the amount of ore, which can be extracted from each mine in a year. 
- The upper limit for mine \var{k} is \var{limit_{k}}.
- The ore from the different mines is of varying quality.
- This quality is measured on a scale so that blending ores together results in a linear combination of the quality measurements, for example, if equal quantities of two ores were combined, the resultant ore would have a quality measurement half way between
that of the ingredient ores. 
- The quality of ore from mine \var{k} is \var{quality_{k}}.
- In each year, it is necessary to combine the total outputs from each mine to produce a blended ore of exactly some stipulated quality.
- In year \var{i}, the required quality is \var{requiredquality_{i}}.
- The final blended ore sells for \var{price} ton each year. 
- Revenue and expenditure for future years must be discounted at a rate of \var{discount} per annum.

INPUT FORMAT:

{
    "n_mines": n_mines,
    "n_maxwork": n_maxwork,
    "royalty": [royalty_{k} for k in 1,...,K],
    "limit": [limit_{k} for k in 1,...,K],
    "quality": [quality_{k} for k in 1,...,K],
    "requiredquality": [requiredquality_{i} for i in 1,...,I],
    "price": price,
    "discount": discount
}


OBJECTIVE: To maximize profit, which mines should be operated each year and how much should they produce?

OUTPUT INFO:

- \var{isoperated} represents whether each mine is operated in each year
- \var{amount} represents the amount of ore produced by each mine in each year

OUTPUT FORMAT:

{
    "isoperated": [[isoperated_{k, i} for i in 1,...,I] for k in 1,...K]
    "amount": [[amount_{k, i} for i in 1,...,I] for k in 1,...K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for MIP Problem}

\subsection*{Parameters:}

\begin{itemize}
    \item $n\_mines$: Number of mines
    \item $n\_maxwork$: Maximum number of mines that can be operated in any one year
    \item $royalty_{k}$: Yearly royalties payable on mine $k$, for $k = 1, \ldots, K$
    \item $limit_{k}$: Upper limit of ore extraction from mine $k$ in a year, for $k = 1, \ldots, K$
    \item $quality_{k}$: Quality of ore from mine $k$, for $k = 1, \ldots, K$
    \item $requiredquality_{i}$: Required quality of blended ore in year $i$, for $i = 1, \ldots, I$
    \item $price$: Selling price per ton of blended ore
    \item $discount$: Discount rate for future cash flows
\end{itemize}

\subsection*{Variables:}

\begin{itemize}
    \item $isoperated_{k, i} \in \{0, 1\}$: Binary variable indicating whether mine $k$ is operated in year $i$
    \item $amount_{k, i} \geq 0$: Amount of ore produced by mine $k$ in year $i$
\end{itemize}

\subsection*{Objective Function:}

Maximize the discounted profit over the years:

\[
\max \sum_{i=1}^{I} \left( \frac{1}{(1 + discount)^i} \left( price \times \sum_{k=1}^{K} amount_{k, i} - \sum_{k=1}^{K} royalty_{k} \times isoperated_{k, i} \right) \right)
\]

\subsection*{Constraints:}

\begin{itemize}
    \item Mining limit constraint for each mine and year:
    \[
    0 \leq amount_{k, i} \leq limit_{k} \times isoperated_{k, i}, \quad \forall k = 1, \ldots, K, \forall i = 1, \ldots, I
    \]

    \item Quality blending constraint for each year:
    \[
    \sum_{k=1}^{K} quality_{k} \times amount_{k, i} = requiredquality_{i} \times \sum_{k=1}^{K} amount_{k, i}, \quad \forall i = 1, \ldots, I
    \]

    \item Maximum number of operated mines constraint for each year:
    \[
    \sum_{k=1}^{K} isoperated_{k, i} \leq n\_maxwork, \quad \forall i = 1, \ldots, I
    \]

    \item Non-negativity constraint for amounts:
    \[
    amount_{k, i} \geq 0, \quad \forall k = 1, \ldots, K, \forall i = 1, \ldots, I
    \]
\end{itemize}

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

\section*{Mathematical Model for MIP Problem}

\subsection*{Parameters:}

\begin{itemize}
    \item $n\_mines$: Number of mines
    \item $n\_maxwork$: Maximum number of mines that can be operated in any one year
    \item $royalty_{k}$: Yearly royalties payable on mine $k$, for $k = 1, \ldots, K$
    \item $limit_{k}$: Upper limit of ore extraction from mine $k$ in a year, for $k = 1, \ldots, K$
    \item $quality_{k}$: Quality of ore from mine $k$, for $k = 1, \ldots, K$
    \item $requiredquality_{i}$: Required quality of blended ore in year $i$, for $i = 1, \ldots, I$
    \item $price$: Selling price per ton of blended ore
    \item $discount$: Discount rate for future cash flows
\end{itemize}

\subsection*{Variables:}

\begin{itemize}
    \item $isoperated_{k, i} \in \{0, 1\}$: Binary variable indicating whether mine $k$ is operated in year $i$
    \item $amount_{k, i} \geq 0$: Amount of ore produced by mine $k$ in year $i$
\end{itemize}

\subsection*{Objective Function:}

Maximize the discounted profit over the years:

\[
\max \sum_{i=1}^{I} \left( \frac{1}{(1 + discount)^i} \left( price \times \sum_{k=1}^{K} amount_{k, i} - \sum_{k=1}^{K} royalty_{k} \times isoperated_{k, i} \right) \right)
\]

\subsection*{Constraints:}

\begin{itemize}
    \item Mining limit constraint for each mine and year:
    \[
    0 \leq amount_{k, i} \leq limit_{k} \times isoperated_{k, i}, \quad \forall k = 1, \ldots, K, \forall i = 1, \ldots, I
    \]

    \item Quality blending constraint for each year:
    \[
    \sum_{k=1}^{K} quality_{k} \times amount_{k, i} = requiredquality_{i} \times \sum_{k=1}^{K} amount_{k, i}, \quad \forall i = 1, \ldots, I
    \]

    \item Maximum number of operated mines constraint for each year:
    \[
    \sum_{k=1}^{K} isoperated_{k, i} \leq n\_maxwork, \quad \forall i = 1, \ldots, I
    \]

    \item Non-negativity constraint for amounts:
    \[
    amount_{k, i} \geq 0, \quad \forall k = 1, \ldots, K, \forall i = 1, \ldots, I
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data_json = '''{
    "n_mines": 4,
    "n_maxwork": 3,
    "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    "quality": [1.0, 0.7, 1.5, 0.5],
    "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0],
    "price": 10,
    "discount": 0.1
}'''

data = json.loads(data_json)

#### Constants
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(n_mines), range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(n_mines), range(n_years)), lowBound=0)

#### Objective function
profit = pulp.lpSum([
    (1 / ((1 + discount) ** (i + 1))) * (price * pulp.lpSum([amount[k][i] for k in range(n_mines)]) -
    pulp.lpSum([royalty[k] * isoperated[k][i] for k in range(n_mines)]))
    for i in range(n_years)
])

problem += profit

#### Constraints

#### Mining limit constraint for each mine and year
for k in range(n_mines):
    for i in range(n_years):
        problem += (amount[k][i] <= limit[k] * isoperated[k][i])

#### Quality blending constraint for each year
for i in range(n_years):
    problem += (pulp.lpSum([quality[k] * amount[k][i] for k in range(n_mines)]) ==
                requiredquality[i] * pulp.lpSum([amount[k][i] for k in range(n_mines)]))

#### Maximum number of operated mines constraint for each year
for i in range(n_years):
    problem += (pulp.lpSum([isoperated[k][i] for k in range(n_mines)]) <= n_maxwork)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

