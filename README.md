# tessah2_final_project

## Project Summary
The tools in this repo will allow you to:
1. Take a .pdf of a philosophy essay and convert it to a .txt file using pdfminer
2. Create a set of background reading recommendations (a set of Stanford Encyclopedia of Philosophy (SEP) page urls) based on a comparison of the word contents of the essay to Stanford Encyclopedia of Philosophy (SEP) entry titles.
3. Perform text mining and sentiment analysis on the philosophy essay, and return graphs and data tables of results, giving an idea of what the common themes of the essay are. 


## Pre-Requisites:
- Homebrew for Mac (or something else that lets you download things)
- Install python (e.g., Mac: brew install python; brew upgrade python)
- Install the necessary python packages (bs4, pandas, etc.) if you haven't already
- Install Jupyter notebook (e.g., brew install jupyter)
- Install R kernel for jupyter notebook (or work with RStudio locally) (https://www.storybench.org/install-r-jupyter-notebook/)
- Chromedriver https://chromedriver.chromium.org/ (must be in the same folder as scraping_and_cleaning.py)
- ***
- Make sure chromedriver is downloaded and is in the same folder location as the python scraper code (https://sites.google.com/a/chromium.org/chromedriver/home)
- Have pdfminer working
  - pdfminer is within this repo, but since it is a repo within a repo, it may not work.  If you need to download and install it locally:
    - https://github.com/euske/pdfminer
    - `pip install pdfminer`
    - make sure the pdfminer repo is in the "philosophizer" folder


## Files and Folders Descriptions

#### pdftotext.py
This python file uses the pdfminer repo to convert a .pdf into a .txt file.  This file is optional, as the user may already have a philosophy essayy in text form.

#### 2_scraping_and_cleaning.py
A python file used to scrape urls from the Stanford Encyclopedia of Philosophy (SEP) table of contents (https://plato.stanford.edu/contents.html).
In addition, it cleans up the data to allow for recommendations to be made based on keywords in the philosophy essay, and encyclopedia page names found in the SEP urls.

#### 3_results.ipynb
A jupyter notebook R file used to output the SEP url background recommendations based on the keywords found in the philosophy essay, as well as further test mining and sentiment analysis completed on the philosophy essay.



## Instructions
Before beginning, be sure to clone the repo.

### Part 1 (Optional): From PDF to .txt with pdfminer
1. From the philosophizer repo, click into the pdfs directory.  
2. You can choose to work with the nagel_bat.pdf example (Thomas Nagel's "What Is It Like To Be a Bat?" essay).  This example is referenced throughout the code and instructions.  Alternatively, you can (1) upload a different philosophy essay pdf into the pdfs folder to work with, or (2) you can skip the pdfs step, and place a text file of a philosophy article in the philosophizer/data folder.  Please note that if you choose not to work with the nagel_bat text, you will have to edit some code.
3. (Mac) Open a command line window, navigate to the philosophizer folder within the repo, and run:
    ```pdf2txt.py -o data/nagel_bat.txt pdfs/nagel_bat.pdf```
    This step uses pdfminer to convert the .pdf into a .txt file, and place the newly created .txt file in the philosophizer/data folder.


### Part 2: Scraping and Cleaning Data
1. (Mac) If you are not there already, open a command line window, navigate to the philosophizer folder within the repo, and run:
    ```python3 2_scraping_and_cleaning.py``` (or ```python 2_scraping_and_cleaning.py```, depending on how you have python set up)
    This script scrapes the list of encyclopedia page urls from the SEP website, and outputs the list into a .txt file (data/encyclo_urls.txt).
    Then, the script takes the list of encyclopedia urls, and extracts the page names from them.  Meanwhile, the philosophy essay is tokenized, and proper nouns are extracted (data/sep_recs.txt) to later compare to the list of page names and their accompanying encyclopedia urls (data/encyclo_titles.csv), and form encyclopedia page recommendations based on the matched keywords found in the philosophy essay.

### Part 3: Results
1. Start Jupyter Notebook by opening a command line window, navigating to the philosophizer folder within the repo, and running:
   ```jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10```
2. In the jupyter notebook browser page opened up by the prior command, open 3_results.ipynb.
3. Click on the Kernel tab, and click "Restart and Run All".
    This R jupyter notebook file outputs the Stanford Encyclopedia of Philosophy page recommendations based on the proper noun content of the philosophy essay.
    Additionally, text mining (word count, co-occurrences, sentient analysis, etc.) is completed on the philosophy essay, giving an idea of what the essay's themes are.


- In addition to being displayed in the notebook upon running it, the data table and data visualization results are saved to philosophizer/results.  
- The encyclopedia background reading url recommendations based on the philosophy essay keywords are located at results/encyclopedia_recommendations.csv
  - For example, based on the content of nagel_bat.txt, 15 urls from the Stanford Encyclopedia of Philosophy are recommended, among them identity, death, and metaphysics.
- The remaining images and .csvs are centered around the text mining and sentiment analysis completed on the philosophy essay.


