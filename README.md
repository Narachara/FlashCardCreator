# FlashCardCreator

**Work in Progress**

Contributions are welcome! If you have suggestions or improvements, feel free to help.

This program generates printable flashcards from an Excel file. Please ensure that the Excel file has the correct number of columns, typically 10 rows (11 with the header). If an image is present in the answer or question column, it will impact the card layout. If the 'small' value is specified in the layout column, the image will maintain its aspect ratio.

Use the template Excel file provided to get started. Note that DinA 7 is not currently supported.

Each cell can hold approximately 100 words with the current font. Make sure to install the following dependencies using pip:

- pandas
- reportlab
- numpy

**Instructions:**

1. Download the necessary files.
2. Fill in the Excel table with pictures and texts.
3. Run the script using the command:
   ```
   ./dinA8.py --inputfile testfile.xlsx --outputfile test.pdf
   ```

