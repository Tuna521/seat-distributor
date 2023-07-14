from PyPDF2 import PdfWriter, PdfReader
from csv import reader

# Open the pdf file of the collective tickets
inputpdf = PdfReader(open("mamma-mia.pdf", "rb"))

# Open the csv to read in each user
customer_info_file = open("Purchase_Summary_Dummy.csv")
customer_info_reader = reader(customer_info_file)
customer_info_header = next(customer_info_reader)
num_customer_header = len(customer_info_header)

# find first name and last name column
i_name = -1
i_surname = -1
i_quantity = -1
cur_i = 0

while cur_i < num_customer_header:
    if (customer_info_header[cur_i] == "First Name"):
        i_name = cur_i
    if (customer_info_header[cur_i] == "Surname"):
        i_surname = cur_i
    if (customer_info_header[cur_i] == "Quantity"):
        i_quantity = cur_i
    cur_i += 1

if i_name == -1:
    raise Exception("csv does not contain \"First Name\" column")
if i_quantity == -1:
    raise Exception("csv does not contain \"First Name\" column")

# Assign pdf and attach the name at the end
# (DOESN'T ACCOUNT THAT TWO TICKETS NEXT TO EACH OTHER (yet))
for i in range(len(inputpdf.pages)):
    customer_info = next(customer_info_reader)

    output = PdfWriter()
    output.add_page(inputpdf.pages[i])
    with open("document-%s-%s.pdf" % (i, customer_info[i_name]), "wb") as outputStream:
        output.write(outputStream)
