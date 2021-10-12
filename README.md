# chess_tournament
Program monitoring scores for a chess tournament, using Swiss pairing algorithm.

## Run program

To run this program:

1. Clone chess_manager_program in our target folder:  
   git clone [https://github.com/Karim-Dorado/Chess_Tournament](https://github.com/Karim-Dorado/Chess_Tournament)    
2. Open your terminal and head to target folder.  
3. Create a virtual environment to install required packages: 
4. Install packages listed in requirements.txt file.    
5. Once required packages have been installed, run command (Windows OS): `python main.py`

# Generate flake8-html report

flake8-html is a flake8 plugin to generate HTML reports of flake8 violations.

To generate flake8-html report:

1. Install flake8-html plugin in your virtual environment (plugin available on [Pypi.org](https://pypi.org/project/flake8-html/) website): `pip install flake8-html` 
2. Run flake8 from the top_level folder of chess_scores_manager program:  

   `flake8 --format=html --htmldir=<report_location>`  

   For instance, if you want to store your report in a folder named "flake_report", run:  

   `flake8 --format=html --htmldir=flake_report`  

   If you want to ignore the presence of a file or a folder when running flake8-html, add `--exclude` option to the command:  

   `flake8 --exclude=<file or folder to exclude> --format=html --htmldir=<name_of_holding_folder>`  
   
   The parameters of flake8 screening (such as maximum line length) are defined in setup.cfg file
