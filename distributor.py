from PyPDF2 import PdfWriter, PdfReader
from csv import reader
from operator import itemgetter

class Distributor:
  
  def __init__(self, seat_row, seat_range, path_to_tickets, path_to_csv, csv_delimiter=','):
    """ 
    Initialize the Seat Distributor.
      :param [str] seat_row: Rows in consequence (ex. ["P", "Q"])
      :param [(int, int)] seat_range: Seat range for each rows (ex. [(16, 25), (17, 21)])
      :param str path_to_tickets: Path to the tickets file, needs to be a pdf file
      :param str csv_file: Path to the csv file of ticket distribution, needs to be a csv file
      :param char csv_delimiter: Set which delimiter csv uses, can be ',' or ';'
      
      :raises ValueError: if csv file does not have "First Name" or "Quantity" header
    """
    self.seat_row = seat_row
    self.seat_range = seat_range
    
    # Open the pdf file of the collective tickets
    self.ticket_file = PdfReader(open(path_to_tickets, "rb"))

    # Open the csv to read in each user
    csv_file = open(path_to_csv, delimiter = csv_delimiter)
    self.csv_reader = reader(csv_file)
    
    self.check_header()
    
    
  def check_header(self):
    # get the header of the csv file
    csv_header = next(self.csv_reader)
    num_header = len(csv_header)
    
    # Find first name and last name column
    self.i_name = -1
    self.i_surname = -1
    self.i_quantity = -1
    i = 0

    # Get needed column and throw error if non-existent
    while i < num_header:
        if (csv_header[i] == "First Name"):
            self.i_name = i
        if (csv_header[i] == "Surname"):
            self.i_surname = i
        if (csv_header[i] == "Quantity"):
            self.i_quantity = i
        i += 1

    if self.i_name == -1:
        raise ValueError("csv does not contain \"First Name\" column")
    if self.i_quantity == -1:
        raise ValueError("csv does not contain \"Quantity\" column")
    
    
  def get_seat_list(self):
    """ 
    Split seats into their own list.
    """
    self.seat_num = [[i for i in range(start, finish + 1)] for (start, finish) in self.seat_range]
    self.seat_taken = [[False for _ in range(start, finish + 1)] for (start, finish) in self.seat_range]
    
  # def distribute_tickets(self):