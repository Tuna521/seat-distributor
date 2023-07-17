from PyPDF2 import PdfWriter, PdfReader
from csv import reader

# The number of rows and seats [included] (ex P16-25, Q17-Q21)
seat_row = ["P", "Q"]
seat_range = [(16, 25), (17, 21)]

# Open the pdf file of the collective tickets
inputpdf = PdfReader(open("mamma-mia.pdf", "rb"))

# Open the csv to read in each user
customer_info_file = open("Purchase_Summary_Dummy.csv")
customer_info_reader = reader(customer_info_file)
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

# Assign pdf and attach the name at the end
# (DOESN'T ACCOUNT THAT TWO TICKETS NEXT TO EACH OTHER (yet))
i = 0

cur_row_i = 0
cur_seat_num = seat_range[cur_row_i][0]
for customer_info in customer_info_reader:
    print(i)
    for n in range(int(customer_info[i_quantity])):
        output = PdfWriter()
        output.add_page(inputpdf.pages[i])
        with open("document-%s%s-%s.pdf" % (seat_row[cur_row_i], cur_seat_num, customer_info[i_name]), "wb") as outputStream:
            output.write(outputStream)
        i += 1
        
        # Get next seat
        cur_seat_num += 1
        if (cur_seat_num > seat_range[cur_row_i][1]):
            cur_row_i += 1
            cur_seat_num = seat_row[cur_row_i][0]