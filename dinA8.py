#! /bin/python3

import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import argparse


# Create the ArgumentParser object
parser = argparse.ArgumentParser(description='Process input and output files.')

# Add the command line arguments
parser.add_argument('--inputfile', help='Path to the input file', required=True)
parser.add_argument('--outputfile', help='Path to the output file', required=True)

# Parse the command line arguments
args = parser.parse_args()

# Access the values of the arguments
INPUTFILE = args.inputfile
OUTPUTFILE = args.outputfile

df = pd.read_excel(INPUTFILE)
c = canvas.Canvas(OUTPUTFILE, pagesize=A4)

# Define overall size
page_width = A4[0]
page_height = A4[1]

# Define card size
# 147 x 210 = A8 
card_width =   210
card_height =   147

# Calculate margin
margin_side =  (page_width - (2 * card_width)) / 2
margin_top_bottom = (page_height - (5 * card_height)) / 2
lower_and_higher_bounds = [i for i in range(40,480,40)] ## for line break arrangement

print(lower_and_higher_bounds)

def cut_and_display_string(col_position, row_position ,input_string, zeilen=12):
    # Find space positions
    stringlen = len(input_string)
    space_positions = [i for i in range(stringlen) if input_string[i].isspace()]
    cut_array = [0]


    # to do:  how do I create a cut array? what if it is of variable length? so it must have at least 24
    # entries for the 12 lines? should I create it before the
    #item > lower && item < upper

    # Calculate vertical positions
    x_positions = [card_height - i for i in range(20, card_height, 10)]

    for i in range(zeilen):
        start = 0 # cut_array[i] # start von zeile
        end = 37 # ende von zeile
        chunk = input_string[start:end].strip()
        display_position = row_position + x_positions[i]
        c.drawString(col_position + 10, display_position, chunk)


def display_string_and_image(Antwort, BildAntwort, row_position,col_position, chunk_size=40):
    #c.drawString(col_position + 20, row_position + (card_height) - 20, Antwort)
    cut_and_display_string(col_position, row_position, Antwort)
    c.drawImage(str(BildAntwort), col_position + 10, row_position + 10, \
        width=card_width - 20, height=card_height - 40, mask=None,
        preserveAspectRatio=True)

def _draw_image(BildAntwort, row_position, col_position, Layout):
    if Layout == 'small':
        print(Layout)
        c.drawImage(str(BildAntwort), col_position + 10, row_position + 10, \
                width=card_width - 20, height=card_height - 20, mask=None,
                preserveAspectRatio=True)
    elif Layout == 'smallbig':
        c.drawImage(str(BildAntwort), col_position + 10, row_position + 10, \
                width=card_width - 20, height=card_height - 20, mask=None,
                preserveAspectRatio=True)
    else:
        c.drawImage(str(BildAntwort), col_position + 10, row_position + 10, \
                width=card_width - 20, height=card_height - 20, mask=None,
                preserveAspectRatio=False)

def writeToPDF(index, row_position, col_position, q_or_a):
    Layout = ''
    BildAntwort = None
    Antwort = None
    if q_or_a == "question":
        BildAntwort = df.iloc[index]['Bild-Frage']
        Antwort = df.iloc[index]['Frage']
        Layout = str(df.iloc[index]['Layout'])
    else:
        BildAntwort = df.iloc[index]['Bild-Antwort']
        Antwort = df.iloc[index]['Antwort']
        Layout = str(df.iloc[index]['Layout'])
    c.rect(col_position, row_position, card_width, card_height)

    if pd.notna(Antwort) and pd.notna(BildAntwort):
        display_string_and_image(Antwort, BildAntwort, row_position,col_position)
    elif pd.isna(Antwort) and pd.notna(BildAntwort):
        _draw_image(BildAntwort, row_position, col_position, Layout)
    elif pd.notna(Antwort) and pd.isna(BildAntwort):
        cut_and_display_string(col_position, row_position, Antwort)
    else:
        raise ValueError("Error: Neither Text nor Bild found for the given index.")


def makeQuestions():
    col_position = margin_side
    row_position = margin_top_bottom
    c.setFont("Helvetica", 10)

    for i in range(10):
        writeToPDF(i, row_position, col_position, "question")
        col_position += card_width
        if (i + 1) % 2 == 0:
            row_position += card_height
            col_position = margin_side


def makeAnswers():
    c.showPage()
    row_position = margin_top_bottom
    col_position = margin_side
    c.setFont("Helvetica", 10)

    for i in range(10):
        match i:
            case 0:
                writeToPDF(1, row_position, col_position, "answer")
            case 1:
                writeToPDF(0, row_position, col_position, "answer")                 
            case 2:
                writeToPDF(3, row_position, col_position, "answer")
            case 3:
                writeToPDF(2, row_position, col_position, "answer")
            case 4:
                writeToPDF(5, row_position, col_position, "answer")
            case 5:
                writeToPDF(4, row_position, col_position, "answer")
            case 6:
                writeToPDF(7, row_position, col_position, "answer")
            case 7:
                writeToPDF(6, row_position, col_position, "answer")
            case 8:
                writeToPDF(9, row_position, col_position, "answer")
            case 9:
                writeToPDF(8, row_position, col_position, "answer")

        col_position += card_width
        if (i + 1) % 2 == 0:
            row_position += card_height
            col_position = margin_side

makeQuestions()
makeAnswers()
c.save()