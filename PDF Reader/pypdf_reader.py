from PyPDF2 import PdfReader
reader = PdfReader("E:\Projects\Image Reader\pdf reader\PDF Files\IMG_0011.pdf")

number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
print(text)