# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- An investor has a portfolio of \var{N} different stocks.
- He has bought \var{bought_i} shares of stock \var{i} at price \var{buyPrice_i}. 
- The current price of one share of stock \var{i} is \var{currentPrice_i}.
- The investor expects that the price of one share of stock \var{i} in one year will be \var{futurePrice_i}.
- If he sells shares, the investor pays transaction costs at the rate of \var{transactionRate} % of the amount transacted.
- In addition, the investor pays taxes at the rate of \var{taxRate} % on capital gains (i.e., the difference between the amount received from selling shares and the amount paid to buy them).
- Both transaction costs and taxes are numbers between 0 and 100.
- The investor wants to raise an amount of money \var{K} net of capital gains and transaction costs.
- You can assume that the investor can sell floating point numbers of shares.

INPUT FORMAT: 

{
    "bought": [bought_i, for i in 1, ..., N],
    "buyPrice": [buyPrice_i, for i in 1, ..., N],
    "currentPrice": [currentPrice_i, for i in 1, ..., N],
    "futurePrice": [futurePrice_i, for i in 1, ..., N],
    "transactionRate": transactionRate,
    "taxRate": taxRate,
    "K": K
}

OBJECTIVE: We want to know how many shares the investor needs to sell in order to raise the needed money, net of capital gains and transaction costs, while maximizing the expected value of his portfolio next year.

OUTPUT INFO:

- \var{sell_i} is the number of shares of stock \var{i} that the investor should sell.

OUTPUT FORMAT:

{
    "sell": [sell_i, for i in 1, ..., N],
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Stock Selling Problem}

\textbf{Parameters:}
\begin{itemize}
    \item \( N \): Number of different stocks
    \item \( bought_i \): Number of shares bought of stock \( i \)
    \item \( buyPrice_i \): Price at which shares of stock \( i \) were bought
    \item \( currentPrice_i \): Current price of one share of stock \( i \)
    \item \( futurePrice_i \): Expected future price of one share of stock \( i \)
    \item \( transactionRate \): Transaction cost rate (in percentage)
    \item \( taxRate \): Tax rate on capital gains (in percentage)
    \item \( K \): Required net amount of money to raise
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( sell_i \): Number of shares of stock \( i \) to be sold
\end{itemize}

\textbf{Objective Function:}
Maximize the expected value of the portfolio next year, which can be expressed as:
\[
\text{Maximize } Z = \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i))
\]

\textbf{Constraints:}
\begin{itemize}
    \item Net amount raised should be equal to \( K \):
    \[
    \sum_{i=1}^{N} \left( (currentPrice_i \cdot sell_i) \cdot \left(1 - \frac{transactionRate}{100}\right) - (buyPrice_i \cdot sell_i) \cdot \frac{taxRate}{100} \right) \geq K
    \]
    
    \item The number of shares sold should not exceed the number of shares bought:
    \[
    sell_i \leq bought_i \quad \forall i \in \{1, 2, \ldots, N\}
    \]
    
    \item Non-negativity constraint:
    \[
    sell_i \geq 0 \quad \forall i \in \{1, 2, \ldots, N\}
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

\section*{Linear Programming Model for Stock Selling Problem}

\textbf{Parameters:}
\begin{itemize}
    \item \( N \): Number of different stocks
    \item \( bought_i \): Number of shares bought of stock \( i \)
    \item \( buyPrice_i \): Price at which shares of stock \( i \) were bought
    \item \( currentPrice_i \): Current price of one share of stock \( i \)
    \item \( futurePrice_i \): Expected future price of one share of stock \( i \)
    \item \( transactionRate \): Transaction cost rate (in percentage)
    \item \( taxRate \): Tax rate on capital gains (in percentage)
    \item \( K \): Required net amount of money to raise
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( sell_i \): Number of shares of stock \( i \) to be sold
\end{itemize}

\textbf{Objective Function:}
Maximize the expected value of the portfolio next year, which can be expressed as:
\[
\text{Maximize } Z = \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i))
\]

\textbf{Constraints:}
\begin{itemize}
    \item Net amount raised should be equal to \( K \):
    \[
    \sum_{i=1}^{N} \left( (currentPrice_i \cdot sell_i) \cdot \left(1 - \frac{transactionRate}{100}\right) - (buyPrice_i \cdot sell_i) \cdot \frac{taxRate}{100} \right) \geq K
    \]
    
    \item The number of shares sold should not exceed the number of shares bought:
    \[
    sell_i \leq bought_i \quad \forall i \in \{1, 2, \ldots, N\}
    \]
    
    \item Non-negativity constraint:
    \[
    sell_i \geq 0 \quad \forall i \in \{1, 2, \ldots, N\}
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from provided JSON
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,
    'TaxRate': 15.0,
    'K': 5000
}

#### Create the LP problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

#### Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=data['Bought'][i]) for i in range(data['N'])]

#### Objective function
problem += pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(data['N'])), "Objective"

#### Constraints
problem += (pulp.lpSum((data['CurrentPrice'][i] * sell[i]) * (1 - data['TransactionRate'] / 100) - 
                       (data['BuyPrice'][i] * sell[i]) * (data['TaxRate'] / 100) 
                       for i in range(data['N'])) >= data['K'], "Net_Amount_Constraint")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

