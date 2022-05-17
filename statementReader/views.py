from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint
from bs4 import BeautifulSoup as bs

from datetime import datetime
from os import listdir


from .models import NetAssetValue
from .models import MarkToMarketPerformanceSummary
from .models import RealizedAndUnrealizedPerformanceSummary
from .models import OpenPositions        
from .models import ForexBalances
from .models import Trades           
from .models import DepositsAndWithdrawals
from .models import Dividends
from .models import WithholdingTax
from .models import InterestAccruals                               
from .models import BaseCurrencyExchangeRate  
from .models import RegisteredStatement



def index(request):

    folder_path = "./statementReader/statement"                # Get all the statement name in folder
    folder_files = listdir(folder_path)

    a = RegisteredStatement.objects.values_list('filename')    # Get statement name in database
    db_files = []
    for k in range(len(a)):
        db_files.append(a[k][0])

    files = []
    for i in range(len(folder_files)):                          # check if the statement is already save in the database
        if folder_files[i] in db_files:                         # if yes. no need to process.
            continue
        files.append(folder_files[i])                           # collection files that are not yet saved in database.
    

    

    # filename = 'U8798920_20220505.htm'
    # filelocation = "Users/waishunwong/Library/Mobile Documents/com~apple~CloudDocs/github/IBStatementManager/statementReader/statement/" + filename
    # browserUrl = "file:///"+filelocation
    # regStatement = RegisteredStatement()
    # regStatement.saveStatement(browserUrl)

    if len(files) == 0:
        msg = "No new statement"
    else:        
        for f in range(len(files)):
            filename = files[f]
            filelocation = "Users/waishunwong/Library/Mobile Documents/com~apple~CloudDocs/github/IBStatementManager/statementReader/statement/"
            Url = "file:///"+filelocation
            regStatement = RegisteredStatement()
            regStatement.saveStatement(Url,filename)
        
        msg = "All files are processed"
    
    return HttpResponse(msg)


