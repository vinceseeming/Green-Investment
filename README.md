# Green-Investment
This project includes a Python Web scraper for parsing 13f filings from SEC's website, [EDGAR](https://www.sec.gov/edgar/search-and-access) and writing them into .csv files. The basic workflow is 1) given the cik number, find the corresponding company's webpage; 2) check if the company discloses 13f forms; 3) if yes, collect the links of filing pages and parse the information table.

The Central Index Key (CIK) is used on the SEC's computer systems to identify corporations and individual people who have filed disclosure with the SEC. I downloaded the current cik lookup data from the SEC website and it included over 777,000 unique cik numbers, but only several thousands of them should report 13f filings.

I gathered 13F filings from 2013 Q2 to 2020 Q4 (since 2013 Q2 the 13f forms are reported in XML file), and the final collection contains 127,474 files.

The data folder in the project only contains the 13f filings of Blackstone Inc. (CIK:0001393818) for the simple test of scraper functionality and the initial exploration on the collected data.
