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

\section*{Mathematical Model for Mining Operations}

\subsection*{Indices and Sets}
\begin{itemize}
    \item $k \in \{1, 2, \dots, n\_mines\}$: Index for mines.
    \item $i \in \{1, 2, \dots, I\}$: Index for years.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $n\_maxwork$: Maximum number of mines that can be operated in any one year.
    \item $royalty_k$: Yearly royalties payable for keeping mine $k$ open.
    \item $limit_k$: Upper limit of ore that can be extracted from mine $k$ in a year.
    \item $quality_k$: Quality of ore from mine $k$.
    \item $requiredquality_i$: Required quality of the blended ore in year $i$.
    \item $price$: Selling price per ton of the blended ore.
    \item $discount$: Discount rate per annum.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $isoperated_{k,i} \in \{0, 1\}$: Binary variable, 1 if mine $k$ is operated in year $i$, 0 otherwise.
    \item $amount_{k,i} \geq 0$: Amount of ore produced by mine $k$ in year $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize the present value of profit over the years:

\[
\text{Maximize} \quad \sum_{i=1}^{I} \frac{1}{(1 + discount)^i} \left( \text{Revenue}_i - \text{Cost}_i \right)
\]

where:

\[
\text{Revenue}_i = price \times \sum_{k=1}^{n\_mines} amount_{k,i}
\]

\[
\text{Cost}_i = \sum_{k=1}^{n\_mines} royalty_k \times isoperated_{k,i}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Blended quality constraint for each year $i$:
    \[
    \sum_{k=1}^{n\_mines} quality_k \times amount_{k,i} = requiredquality_i \times \sum_{k=1}^{n\_mines} amount_{k,i}
    \]

    \item Ore production limit for each mine $k$ and year $i$:
    \[
    amount_{k,i} \leq limit_k \times isoperated_{k,i}
    \]

    \item Maximum number of mines operated in each year $i$:
    \[
    \sum_{k=1}^{n\_mines} isoperated_{k,i} \leq n\_maxwork
    \]

    \item Non-negativity constraint for ore amount:
    \[
    amount_{k,i} \geq 0
    \]

    \item Binary constraint for operation:
    \[
    isoperated_{k,i} \in \{0, 1\}
    \]
\end{itemize}

\subsection*{Output}
The output includes the operation status of each mine and their production levels for each year.

\begin{itemize}
    \item $isoperated = [[isoperated_{k,i} \text{ for } i \text{ in } 1,\ldots,I] \text{ for } k \text{ in } 1,\ldots,K]$
    \item $amount = [[amount_{k,i} \text{ for } i \text{ in } 1,\ldots,I] \text{ for } k \text{ in } 1,\ldots,K]$
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

\section*{Mathematical Model for Mining Operations}

\subsection*{Indices and Sets}
\begin{itemize}
    \item $k \in \{1, 2, \dots, n\_mines\}$: Index for mines.
    \item $i \in \{1, 2, \dots, I\}$: Index for years.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $n\_maxwork$: Maximum number of mines that can be operated in any one year.
    \item $royalty_k$: Yearly royalties payable for keeping mine $k$ open.
    \item $limit_k$: Upper limit of ore that can be extracted from mine $k$ in a year.
    \item $quality_k$: Quality of ore from mine $k$.
    \item $requiredquality_i$: Required quality of the blended ore in year $i$.
    \item $price$: Selling price per ton of the blended ore.
    \item $discount$: Discount rate per annum.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $isoperated_{k,i} \in \{0, 1\}$: Binary variable, 1 if mine $k$ is operated in year $i$, 0 otherwise.
    \item $amount_{k,i} \geq 0$: Amount of ore produced by mine $k$ in year $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize the present value of profit over the years:

\[
\text{Maximize} \quad \sum_{i=1}^{I} \frac{1}{(1 + discount)^i} \left( \text{Revenue}_i - \text{Cost}_i \right)
\]

where:

\[
\text{Revenue}_i = price \times \sum_{k=1}^{n\_mines} amount_{k,i}
\]

\[
\text{Cost}_i = \sum_{k=1}^{n\_mines} royalty_k \times isoperated_{k,i}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Blended quality constraint for each year $i$:
    \[
    \sum_{k=1}^{n\_mines} quality_k \times amount_{k,i} = requiredquality_i \times \sum_{k=1}^{n\_mines} amount_{k,i}
    \]

    \item Ore production limit for each mine $k$ and year $i$:
    \[
    amount_{k,i} \leq limit_k \times isoperated_{k,i}
    \]

    \item Maximum number of mines operated in each year $i$:
    \[
    \sum_{k=1}^{n\_mines} isoperated_{k,i} \leq n\_maxwork
    \]

    \item Non-negativity constraint for ore amount:
    \[
    amount_{k,i} \geq 0
    \]

    \item Binary constraint for operation:
    \[
    isoperated_{k,i} \in \{0, 1\}
    \]
\end{itemize}

\subsection*{Output}
The output includes the operation status of each mine and their production levels for each year.

\begin{itemize}
    \item $isoperated = [[isoperated_{k,i} \text{ for } i \text{ in } 1,\ldots,I] \text{ for } k \text{ in } 1,\ldots,K]$
    \item $amount = [[amount_{k,i} \text{ for } i \text{ in } 1,\ldots,I] \text{ for } k \text{ in } 1,\ldots,K]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parameters
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 
        'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 
        'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

n_mines = data['n_mines']
n_years = len(data['requiredquality'])
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

#### Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

#### Problem
problem = pulp.LpProblem("Mining_Operations", pulp.LpMaximize)

#### Objective Function
revenue = {i: price * pulp.lpSum(amount[k, i] for k in range(n_mines)) for i in range(n_years)}
cost = {i: pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines)) for i in range(n_years)}
present_value_profit = pulp.lpSum((revenue[i] - cost[i]) / ((1 + discount) ** i) for i in range(n_years))
problem += present_value_profit

#### Constraints
#### Blended quality constraint
for i in range(n_years):
    problem += (pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) ==
                requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines)))

#### Ore production limit for each mine and year
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

#### Maximum number of mines operated in each year
for i in range(n_years):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

#### Solve the problem
problem.solve()

#### Output results
isoperated_output = [[pulp.value(isoperated[k, i]) for i in range(n_years)] for k in range(n_mines)]
amount_output = [[pulp.value(amount[k, i]) for i in range(n_years)] for k in range(n_mines)]

print("Operation Status (0=Not operated, 1=Operated):")
for k in range(n_mines):
    print(f"Mine {k+1}: {isoperated_output[k]}")

print("\nAmount of Ore Produced:")
for k in range(n_mines):
    print(f"Mine {k+1}: {amount_output[k]}")

print(f'\n (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

