## Wolt Coding Task

In this repo is the implemtation for wolt coding task at: https://github.com/woltapp/summer2019

## Installation

```pipenv install``` to restore package


## Execution

```
$ pipenv run python main.py --help                                            

Usage: main.py [OPTIONS]                                                      
                                                                              
Options:                                                                      
  --startdate TEXT  Required. Starting date of the analysis period. Format: dd-mm-yyy e.g. 01-11-2019                                 
  --enddate TEXT    Optional. Ending date of the analysis period. Format: dd-mm-yyy e.g. 01-11-2019. Default to starting date 
  --hours TEXT      Optional. Delivery hours for analysis. Format: hh-hh e.g. 07-22 (inclusive). Default to 00-24 
  --help            Show this message and exit.                               
```

### Examples
```pipenv run python main.py --startdate=07-01-2019```  
```pipenv run python main.py --startdate=07-01-2019 --enddate=09-01-2019```  
```pipenv run python main.py --startdate=07-01-2019 --enddate=09-01-2019 --hours=11-15```

### Alternative

Alternatively you can use ```pip install -r requirements.txt``` and execute the program with just ```python main.py [Options]```, however beware that this can affect your current python environment. 