from PyPDF2 import PdfWriter, PdfReader
from csv import reader
from operator import itemgetter

# The number of rows and seats [included] (ex P16-25, Q17-Q21)
seat_row = ["P", "Q"]
seat_range = [(16, 24), (17, 21)]

# Expand seat range into its individual cell
seat_range_all = [[i for i in range(start, finish + 1)] for (start, finish) in seat_range]
seat_taken = [[False for _ in range(start, finish + 1)] for (start, finish) in seat_range]

# Open the pdf file of the collective tickets
inputpdf = PdfReader(open("mamma-mia.pdf", "rb"))

# Open the csv to read in each user
customer_info_file = open("Purchase_Product_Mamma_Mia.csv")  #  append ",delimiter=',')" if needed
customer_info_reader = reader(customer_info_file)

# get the header of the csv file
customer_info_header = next(customer_info_reader)
num_customer_header = len(customer_info_header)

# Find first name and last name column
i_name = -1
i_surname = -1
i_quantity = -1
i = 0

# Get needed column and throw error if non-existent
while i < num_customer_header:
    if (customer_info_header[i] == "First Name"):
        i_name = i
    if (customer_info_header[i] == "Surname"):
        i_surname = i
    if (customer_info_header[i] == "Quantity"):
        i_quantity = i
    i += 1

if i_name == -1:
    raise Exception("csv does not contain \"First Name\" column")
if i_quantity == -1:
    raise Exception("csv does not contain \"Quantity\" column")

# Sort the table by number of tickets ordered
customer_info_reader = sorted(customer_info_reader, key=itemgetter(i_quantity), reverse=True)

# Assign pdf and attach the name at the end
# (DOESN'T ACCOUNT THAT TWO TICKETS NEXT TO EACH OTHER (yet))

cur_row = 0
for customer_info in customer_info_reader:
    print(customer_info)
    init_row = cur_row
    first_occurance = seat_taken[cur_row].index(False)
    quantity = int(customer_info[i_quantity])
    
    can_allocate = True
    found = False
    if int(customer_info[i_quantity]) > 1:
        # check that the row doesnt have 3 at then end,
        # if it does, try allocating a block in next row and do the check again
        # if we got to the last row and cannot do so, go back to the first row and give the continous seats
        # if there is only one seat, go to next row
        while not found:
        
        # (first_occurance >= len(seat_taken[cur_row]) - 3 and can_allocate) or (first_occurance >= len(seat_taken[cur_row]) - quantity and not can_allocate):
 
            first_occurance = seat_taken[cur_row].index(False)
            
            if (can_allocate and first_occurance < len(seat_taken[cur_row]) - 3) or (not can_allocate and first_occurance < len(seat_taken[cur_row]) - quantity):
                found = True
            
            if (first_occurance == -1 or (can_allocate and first_occurance >= len(seat_taken[cur_row]) - 3)):
                if (cur_row == len(seat_row)):
                    cur_row = 0
                    can_allocate = False
                else:
                    cur_row += 1
                
                
            # TODO: Bug where it will be index error if you canot find 3 in row
            
            if (cur_row == init_row):
                # allocate any as long as there is two next to each other
                if int(customer_info[i_quantity]) >= len(seat_taken[cur_row]) - first_occurance:
                    raise Exception("There is no more seats!")
        
        page_num = sum([seat_range[i][1] - seat_range[i][0] + 1 for i in range(cur_row)]) + first_occurance
        
        for i in range(int(customer_info[i_quantity])):
            output = PdfWriter()
            output.add_page(inputpdf.pages[page_num])
            with open("document-%s%s-%s.pdf" % (seat_row[cur_row], seat_range_all[cur_row][first_occurance], customer_info[i_name]), "wb") as outputStream:
                output.write(outputStream)
                
            seat_taken[cur_row][first_occurance] = True
            first_occurance += 1
            page_num += 1
                
    else:
        # just allocate first free
        # Throw exception if cannot find a free seat
        # TODO: return to the first one if needed
        init_row = seat_row[0]
        while (first_occurance == -1):
            cur_row += 1
            first_occurance = seat_taken[cur_row].index(False)
            if (cur_row == len(seat_row)): 
                cur_row = 0
            if (cur_row == init_row):
                raise Exception("There is no more seats")
                
            
        page_num = sum([seat_range[i][1] - seat_range[i][0] + 1 for i in range(cur_row)]) + first_occurance
        
        output = PdfWriter()
        output.add_page(inputpdf.pages[page_num])
        with open("document-%s%s-%s.pdf" % (seat_row[cur_row], seat_range_all[cur_row][first_occurance], customer_info[i_name]), "wb") as outputStream:
            output.write(outputStream)
            
        seat_taken[cur_row][first_occurance] = True
# i = 0

# cur_row_i = 0
# cur_seat_num = seat_range[cur_row_i][0]
# for customer_info in customer_info_reader:
#     print(i)
#     for n in range(int(customer_info[i_quantity])):
#         output = PdfWriter()
#         output.add_page(inputpdf.pages[i])
#         with open("document-%s%s-%s.pdf" % (seat_row[cur_row_i], cur_seat_num, customer_info[i_name]), "wb") as outputStream:
#             output.write(outputStream)
#         i += 1
        
#         # Get next seat
#         cur_seat_num += 1
#         if (cur_seat_num > seat_range[cur_row_i][1]):
#             cur_row_i += 1
#             cur_seat_num = seat_row[cur_row_i][0]