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
    
    # self.seat_num = [[i for i in range(start, finish + 1)] for (start, finish) in seat_range]
    self.seat_taken = [[False for _ in range(start, finish + 1)] for (start, finish) in seat_range]
    
    self.ticket_file = PdfReader(open(path_to_tickets, "rb"))

    csv_file = open(path_to_csv, delimiter = csv_delimiter)
    self.csv_reader = reader(csv_file)
    
    (self.i_name, self.i_surname, self.i_quantity) = self.get_header_index()
    
    # Sort the table by number of tickets ordered
    self.csv_reader = sorted(self.csv_reader, key=itemgetter(self.i_quantity), reverse=True)
    
    
  def get_header_index(self):
    """ 
    Gets index of the header corresponding to "First Name", "Surname", and "Quantity".
     
      :return: index of headers (in order) for "First Name", "Surname", and "Quantity" 
      :rtype: (int, int, int)
      :raises ValueError: if csv file does not have "First Name" or "Quantity" header
    """
    self.csv_header = next(self.csv_reader)
    num_header = len(self.csv_header)
    
    # Find first name and last name column
    i_name = -1
    i_surname = -1
    i_quantity = -1
    i = 0

    # Get needed column and throw error if non-existent
    while i < num_header:
        if (self.csv_header[i] == "First Name"):
            i_name = i
        if (self.csv_header[i] == "Surname"):
            i_surname = i
        if (self.csv_header[i] == "Quantity"):
            i_quantity = i
        i += 1

    if i_name == -1:
        raise ValueError("csv does not contain \"First Name\" column")
    if i_quantity == -1:
        raise ValueError("csv does not contain \"Quantity\" column")
      
    return (i_name, i_surname, i_quantity)
     
     
  def first_free_seat_in_row(self, row) -> int:
    """
    Returns first free seat number index in that row (ex returns 2 for seat 22 for range (20-25)).
      
      :param int row: Index of the row (corresponding in seat_row)
      :return: index of first free seat in row
      :rtype: int
    """
    return self.seat_taken[row].index(False) 
    
    
  def number_of_seats_in_row(self, row) -> int:
    """ 
    Returns number of seats in given row. 
    """
    return self.get_lowest_seat_num(row) - self.get_highest_seat_num(row) + 1

    
  def get_lowest_seat_num(self, row) -> int:
    """ 
    Returns the lowest seat number that is available in the given row. 
    """
    return self.seat_range[row][0]
  
  
  def get_highest_seat_num(self, row) -> int:
    """ 
    Returns the highest seat number that is available in the given row. 
    """
    return self.seat_range[row][1]
    
    
  def get_page_num(self, row, seat) -> int:
    """ 
    Returns page number in the pdf tickets file corresponding to the row and seat number.
    
      :param int row: Index of the row (corresponding in seat_row)
      :param int seat: Index of the seat (ex. returns 2 for the 2nd available seat in the row)
      :return: index of first free seat in row
      :rtype: int
    """
    return sum([self.number_of_seats_in_row(r) for r in range(row)]) + seat
    
    
    
  def find_first_free_seat(self, init_row, ones, quantity = 1) -> (int, int):
    """ Returns row and index """
    first_free = self.first_free_seat_in_row(cur_row)
    if quantity > 1:
        # case when ticket more than one
        while first_free > self.number_of_seats_in_row(cur_row) - ones:
          cur_row += 1
          first_free = self.first_free_seat_in_row(cur_row)
          
          if (cur_row == len(self.seat_row)):
              cur_row = 0
          if (cur_row == init_row):
              if quantity >= self.number_of_seats_in_row(cur_row) - first_free:
                  raise Exception("There is no more seats!")
    
  def create_pdf_ticket(self, row, first_free, customer):
    """
    Creates the individual ticket for the given row, index, and name
    """
    
    page_num = self.get_page_num(row, first_free)
          
    output = PdfWriter()
    output.add_page(self.ticket_file.pages[page_num])
    with open("document-%s%s-%s.pdf" % (self.seat_row[row], self.get_lowest_seat_num(row) + first_free, customer[self.i_name]), "wb") as outputStream:
        output.write(outputStream)
        
    self.seat_taken[row][first_free] = True
    
    
  def distribute_tickets(self, ones=3):
    """
    Distributes the seats, so that people that bought one tickets sit next to each other if they can.
    
      :param int ones: Number of people with single tickets to be grouped together
    """
    cur_row = 0
    for customer in self.csv_reader:
      
      init_row = cur_row
      quantity = int(customer[self.i_quantity])
      
      first_free = self.first_free_seat_in_row(cur_row)
      # Refactor into its own function ----------
      if quantity > 1:
        # case when ticket more than one
        while first_free > self.number_of_seats_in_row(cur_row) - ones:
          cur_row += 1
          first_free = self.first_free_seat_in_row(cur_row)
          
          if (cur_row == len(self.seat_row)):
              cur_row = 0
          if (cur_row == init_row):
              if quantity >= self.number_of_seats_in_row(cur_row) - first_free:
                  raise Exception("There is no more seats!")
      # ---------------------------------------
        
      if quantity > 1:
        for i in range(quantity):
          self.create_pdf_ticket(cur_row, first_free, customer)
          first_free += 1
        
      else:
        #  case when tickets is one
        print("todo")
        
        
           
           
seat_row = ["P", "Q"]
seat_range = [(16, 25), (17, 21)]
path_to_tickets = "mamma-mia.pdf"
path_to_csv = "Purchase_Summary_Mamma_Mia.csv"
 
distributor = Distributor(seat_row, seat_range, path_to_tickets, path_to_csv)
distributor.distribute_tickets()