<h3 align="center">Seat Distributor</h3>

## About the Project

This repository distributes the seats to the customers according to the spreadsheet, creating a folder of individual tickets to assigned person.

It makes sure that people that came alone sit together so they can socialize.

This was created initially for Imperial ArtSoc to accelerate the process of distributing tickets to the shows.

### Built With

- Python
- PyPDF2 library
- csv library

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- PyPDF2

```sh
pip install PyPDF2
```

### Installation

1. Clone the repo

```ssh
git clone https://github.com/Tuna521/seat-distributor.git
```

2. In the folder drag the pdf of the tickets file (should be in order)

3. Add the csv file with the csv information of the customers
   Important: it need to contain column with "First Name" and "Quantity"

4. Open `distributor.py`, scroll down to the end of file, and modify these lines accroding to your seat range (line 191-192)

Example: Tickets from (all inclusive) P16-P25, Q17-Q21

```python
seat_row = ["P", "Q"]
seat_range = [(16, 25), (17, 21)]
```

5. Modify the lines after to add file names for the ticket and csv file as they are in the folder

```python
path_to_tickets = "mamma-mia.pdf"
path_to_csv = "Purchase_Product_Mamma_Mia.csv"
```
