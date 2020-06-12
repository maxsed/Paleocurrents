# Paleocurrents
Python code for converting paleocurrent measurements and plotting in (equal-area) rose diagrams.

The current version only converts imbrication measurements, and handles single-sheet excel files only.
Updated versions will:
- increase efficiency
- be more user-friendly
- handle more types of measurements (e.g. planar x-lamination, trough x-lamination)
- let the user choose between dip/dipdirection, strike/dip, direct measurement
- handle excel files with multiple sheets

INPUT: Excel datasheet with measurements of dip/dipdirection of paeocurrent indicators. Column names should be changed either in the excel file or directly iin the code.

VARIABLES: number of bins, equal-area [True/False], 

OUTPUT: Rose diagrams
