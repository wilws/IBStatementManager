from django.db import models
from datetime import datetime
from pprint import pprint
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


# Create your models here.


class NetAssetValue(models.Model):
    date = models.DateField()
    long = models.DecimalField(max_digits=19, decimal_places=4)
    short = models.DecimalField(max_digits=19, decimal_places=4)
    asset = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)


    def extraction(self,d,e):

        assetGroup = d.find("tbody").find_all('tr')
        asset = []

        for i in range(len(assetGroup)):

            _content = assetGroup[i].find_all('td')
            _name = BSString(_content[0])

            if _name == "Total":
                break

            self.pk = None
            self.asset=_name
            self.date=e
            self.long=BSFloat(_content[2])
            self.short=BSFloat(_content[3])
            self.save()
    
    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Net Asset Value Report on {d}"

        
class MarkToMarketPerformanceSummary(models.Model):

    symbol = models.CharField(max_length=100)
    assetClass = models.CharField(max_length=100)
    qty = models.DecimalField(max_digits=19, decimal_places=4)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    position = models.DecimalField(max_digits=19, decimal_places=4)
    transaction = models.DecimalField(max_digits=19, decimal_places=4)
    commissions = models.DecimalField(max_digits=19, decimal_places=4)
    other = models. CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)


    def extraction(self,d,e):

        assetPool = d.find("tbody").find_all('tr')
        asset = []
        assetclass = ""
        for i in range(len(assetPool)):

            _content = assetPool[i].find_all('td')

            if _content[0].has_attr('class'):
               
                _className = _content[0]["class"][0]
                if _className == "indent":
                    continue
                if _className == "header-asset":
                    assetclass = BSString(_content[0])
                    continue

            if BSString(_content[0]) == "Broker Interest Paid and Received":
                continue
                

            self.pk = None
            self.symbol = BSString(_content[0])
            self.assetClass = assetclass
            self.qty = BSFloat(_content[2])
            self.price = BSFloat(_content[4])
            self.position = BSFloat(_content[5])
            self.transaction = BSFloat(_content[6])
            self.commissions = BSFloat(_content[7])
            self.other = BSFloat(_content[8])
            self.date = e
            self.save()

    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Mark To Market Summary Report on {d}"


class RealizedAndUnrealizedPerformanceSummary(models.Model):

    symbol = models.CharField(max_length=100)
    assetClass = models.CharField(max_length=100)
    cost_adj = models.DecimalField(max_digits=19, decimal_places=4)
    rlz_ST_profit = models.DecimalField(max_digits=19, decimal_places=4)
    rlz_ST_loss = models.DecimalField(max_digits=19, decimal_places=4)
    rlz_LT_profit = models.DecimalField(max_digits=19, decimal_places=4)
    rlz_LT_loss = models.DecimalField(max_digits=19, decimal_places=4)
    unrlz_ST_profit = models.DecimalField(max_digits=19, decimal_places=4)
    unrlz_ST_loss = models.DecimalField(max_digits=19, decimal_places=4)
    unrlz_LT_profit = models.DecimalField(max_digits=19, decimal_places=4)
    unrlz_LT_loss = models.DecimalField(max_digits=19, decimal_places=4)
    date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)

    def extraction(self,d,e):
    
        assetPool = d.find("tbody").find_all('tr')
        asset = []
        assetclass = ""
        for i in range(len(assetPool)):

            _content = assetPool[i].find_all('td')


            if _content[0].has_attr('class'):
                _className = _content[0]["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "indent":
                    continue
                if _className == "header-asset":
                    assetclass = BSString(_content[0])
                    continue

                
            self.pk = None
            self.symbol = BSString(_content[0])
            self.assetClass = assetclass
            self.cost_adj = BSFloat(_content[1])
            self.rlz_ST_profit = BSFloat(_content[2])
            self.rlz_ST_loss = BSFloat(_content[3])
            self.rlz_LT_profit = BSFloat(_content[4])
            self.rlz_LT_loss = BSFloat(_content[5])
            self.unrlz_ST_profit = BSFloat(_content[7])
            self.unrlz_ST_loss = BSFloat(_content[8])
            self.unrlz_LT_profit = BSFloat(_content[9])
            self.unrlz_LT_loss = BSFloat(_content[10])
            self.date = e
            self.save()


    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Realized And Unrealized Performance Summary on {d}"
 

class OpenPositions(models.Model):

    symbol = models.CharField(max_length=100)
    assetClass = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=19, decimal_places=4)
    mult = models.DecimalField(max_digits=19, decimal_places=4)
    cost_price = models.DecimalField(max_digits=19, decimal_places=4)
    cost_basis = models.DecimalField(max_digits=19, decimal_places=4)
    close_price = models.DecimalField(max_digits=19, decimal_places=4)
    value = models.DecimalField(max_digits=19, decimal_places=4)
    unrealized_PL = models.DecimalField(max_digits=19, decimal_places=4)
    code = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)


    def extraction(self,d,e):

        assetPool = d.find_all("tbody")
        asset = []
        assetclass = ""
        currency = ""

        for i in range(len(assetPool)):

            _tr = assetPool[i].tr

            if _tr.has_attr('class'):
                _className = _tr["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "total":
                    continue

            if _tr.td.has_attr('class'):
                _className = _tr.td["class"][0]
                if _className == "header-asset":
                    assetclass = BSString(_tr.td)
                    continue
                if _className == "header-currency":
                    currency = BSString(_tr.td)
                    continue

            _content = _tr.find_all("td")
            
            
            self.pk = None
            self.symbol = BSString(_content[0])
            self.assetClass = assetclass
            self.currency = currency
            self.quantity = BSFloat(_content[1])
            self.mult = BSFloat(_content[2])
            self.cost_price = BSFloat(_content[3])
            self.cost_basis = BSFloat(_content[4])
            self.close_price = BSFloat(_content[5])
            self.value = BSFloat(_content[6])
            self.unrealized_PL = BSFloat(_content[7])
            self.code = BSString(_content[8])
            self.date = e
            self.save()

    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Open Positions on {d}"
 
              
class ForexBalances(models.Model):

    symbol = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=19, decimal_places=4)
    cost_price = models.DecimalField(max_digits=19, decimal_places=4)
    cost_Basis_HKD = models.DecimalField(max_digits=19, decimal_places=4)
    close_price = models.DecimalField(max_digits=19, decimal_places=4)
    value_HKD = models.DecimalField(max_digits=19, decimal_places=4)
    unrealized_HKD = models.DecimalField(max_digits=19, decimal_places=4)
    code = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)


    def extraction(self,d,e):

        assetPool = d.find_all("tbody")
        asset = []
        assetclass = ""
        currency = ""

        for i in range(len(assetPool)):

            _tr = assetPool[i].tr

            if _tr.has_attr('class'):
                _className = _tr["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "total":
                    continue

            if _tr.td.has_attr('class'):
                _className = _tr.td["class"][0]
                if _className == "header-asset":
                    assetclass = BSString(_tr.td)
                    continue
                if _className == "header-currency":
                    currency = BSString(_tr.td)
                    continue

            _content = _tr.find_all("td")

            self.pk = None
            self.symbol = BSString(_content[0])
            self.quantity = BSFloat(_content[1])
            self.cost_price = BSFloat(_content[2])
            self.cost_Basis_HKD = BSFloat(_content[3])
            self.close_price = BSFloat(_content[4])
            self.value_HKD = BSFloat(_content[5])
            self.unrealized_HKD = BSFloat(_content[6])
            self.code = BSString(_content[7])
            self.date = e
            self.save()


    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Forex Balances on {d}"

    
class Trades(models.Model):                

    symbol = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    assetClass = models.CharField(max_length=100)
    date_Time = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=19, decimal_places=4)
    trade_price = models.DecimalField(max_digits=19, decimal_places=4)
    close_price = models.DecimalField(max_digits=19, decimal_places=4)
    proceeds = models.DecimalField(max_digits=19, decimal_places=4)
    comm_Fee = models.DecimalField(max_digits=19, decimal_places=4)
    basis = models.DecimalField(max_digits=19, decimal_places=4)
    realized_pl = models.DecimalField(max_digits=19, decimal_places=4)
    mtm_pl = models.DecimalField(max_digits=19, decimal_places=4)
    code = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)


    def forexHandling(self,d,e):
        assetPool = d.find_all("tbody")
        asset = []
        assetclass = ""
        currency = ""

        for i in range(len(assetPool)):

            _tr = assetPool[i].tr

            if _tr.has_attr('class'):
                _className = _tr["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "total":
                    continue

            if _tr.td.has_attr('class'):
                _className = _tr.td["class"][0]
                if _className == "header-asset":
                    assetclass = BSString(_tr.td)
                    continue
                if _className == "header-currency":
                    currency = BSString(_tr.td)
                    continue

            _content = _tr.find_all("td")

            self.pk = None
            self.symbol = BSString(_content[0])
            self.currency = currency
            self.assetClass = "Forex"
            self.date_Time = BSString(_content[1])
            self.quantity = BSFloat(_content[2])
            self.trade_price = BSFloat(_content[3])
            self.close_price = 0
            self.proceeds = BSFloat(_content[5])
            self.comm_Fee = BSFloat(_content[6])
            self.basis = 0
            self.realized_pl = 0
            self.mtm_pl = BSFloat(_content[7])
            self.code = BSString(_content[8])
            self.date = e
            self.save()
  


    def extraction(self,d,e):

        assetPool = d.find_all("tbody")
        asset = []
        assetclass = ""
        currency = ""

        for i in range(len(assetPool)):

            _tr = assetPool[i].tr

            if BSString(_tr.td) == "Forex":
                self.forexHandling(d,e)
                break

            if _tr.has_attr('class'):
                _className = _tr["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "total":
                    continue

            if _tr.td.has_attr('class'):
                _className = _tr.td["class"][0]
                if _className == "header-asset":
                    assetclass = BSString(_tr.td)
                    continue
                if _className == "header-currency":
                    currency = BSString(_tr.td)
                    continue

            _content = _tr.find_all("td")

            self.pk = None
            self.symbol = BSString(_content[0])
            self.currency = currency
            self.assetClass = assetclass
            self.date_Time = BSString(_content[1])
            self.quantity = BSFloat(_content[2])
            self.trade_price = BSFloat(_content[3])
            self.close_price = BSFloat(_content[4])
            self.proceeds = BSFloat(_content[5])
            self.comm_Fee = BSFloat(_content[6])
            self.basis = BSFloat(_content[7])
            self.realized_pl = BSFloat(_content[8])
            self.mtm_pl = BSFloat(_content[9])
            self.code = BSString(_content[10])
            self.date = e
            self.save()
  

    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Trade Report on {d}"


class DepositsAndWithdrawals(models.Model):   

    date = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    report_date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)

    def extraction(self,d,e):
    
        assetPool = d.find("tbody").find_all('tr')
        asset = []
        currency = ""

        for i in range(len(assetPool)):

            _content = assetPool[i].find_all('td')

            if _content[0].has_attr('class'):
                _className = _content[0]["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "indent":
                    continue
                if _className == "header-currency":
                    currency = BSString(_content[0])
                    continue

            self.pk = None
            self.date=BSString(_content[0])
            self.currency=currency
            self.description=BSString(_content[1])
            self.amount=BSFloat(_content[2])
            self.report_date = e
            self.save()
            
    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Deposits And Withdrawals Report on {d}"


class Dividends(models.Model):

    date = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    report_date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)


    def extraction(self,d,e):

        assetPool = d.find("tbody").find_all('tr')
        asset = []
        currency = ""

        for i in range(len(assetPool)):

            _content = assetPool[i].find_all('td')

            if _content[0].has_attr('class'):
                _className = _content[0]["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "indent":
                    continue
                if _className == "header-currency":
                    currency = BSString(_content[0])
                    continue

            self.pk = None
            self.date = BSString(_content[0])
            self.currency = currency
            self.description = BSString(_content[1])
            self.amount = BSFloat(_content[2])
            self.report_date = e
            self.save()

            
    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Dividend Report on {d}"   


class WithholdingTax(models.Model):    

    date = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    report_date = models.DateField()
    code = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)


    def extraction(self,d,e):
        assetPool = d.find("tbody").find_all('tr')
        asset = []
        currency = ""

        for i in range(len(assetPool)):

            _content = assetPool[i].find_all('td')

            if _content[0].has_attr('class'):
                _className = _content[0]["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "indent":
                    continue
                if _className == "header-currency":
                    currency = BSString(_content[0])
                    continue

            
            self.pk = None
            self.date = BSString(_content[0])
            self.currency = currency
            self.description =  BSString(_content[1])
            self.amount = BSFloat(_content[2])
            self.report_date = e
            self.code = BSString(_content[3])
            self.save()

            
    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Withholding Tax Report on {d}" 


class InterestAccruals(models.Model):                                  

    accrual_reversal = models.DecimalField(max_digits=19, decimal_places=4)
    date = models.DateField()
    ending_accrual_balance = models.DecimalField(max_digits=19, decimal_places=4)
    ending_accrual_balance_in_hkd = models.DecimalField(max_digits=19, decimal_places=4)
    fx_translation = models.DecimalField(max_digits=19, decimal_places=4)
    interest_accrued = models.DecimalField(max_digits=19, decimal_places=4)
    starting_accrual_balance = models.DecimalField(max_digits=19, decimal_places=4)
    symbol = models.CharField(max_length=100)

    def extraction(self,d,e):

        assetPool = d.find("tbody").find_all('tr')
        asset = []
        symbol = ""

        for i in range(len(assetPool)):

            _content = assetPool[i].find_all('td')

            if _content[0].has_attr('class'):
                _className = _content[0]["class"][0]
                if _className == "subtotal":
                    continue
                if _className == "header-currency":
                    
                    if len(symbol) >0 :
                        self.saveObj(_dict,e)

                    symbol = BSString(_content[0])
                    _dict = {}
                    _dict['symbol'] = symbol
                    _dict['date'] = e
                    continue
                
            _key = BSString(_content[0]).lower().replace(" ","_")
            _dict[_key] = BSFloat(_content[1])
        
        self.saveObj(_dict,e)


    def saveObj(self,d,e):

        self.pk = None
        self.accrual_reversal = d['accrual_reversal']
        self.date = d['date']
        self.ending_accrual_balance = d['ending_accrual_balance']
        if "ending_accrual_balance_in_hkd" not in d:
            d['ending_accrual_balance_in_hkd'] = 0
        self.ending_accrual_balance_in_hkd = d['ending_accrual_balance_in_hkd']
        if "fx_translation" not in d:
            d['fx_translation'] = 0
        self.fx_translation = d['fx_translation']
        self.interest_accrued = d['interest_accrued']
        self.starting_accrual_balance = d['starting_accrual_balance']
        self.symbol = d['symbol']
        self.save()

 

            
    def __str__(self):
        d = datetime.strftime(self.date,"%m/%d/%Y")
        return f"Interest Accruals Report on {d}" 


class BaseCurrencyExchangeRate(models.Model):     


    GBP = models.DecimalField(max_digits=19, decimal_places=4)
    USD = models.DecimalField(max_digits=19, decimal_places=4)
    date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)

    def extraction(self,d,e):
        
        self.GBP = BSFloat(d.find("td",string="GBP").find_next("td"))
        self.USD = BSFloat(d.find("td",string="USD").find_next("td"))
        self.date = e
        self.save()



class RegisteredStatement(models.Model):
    date = models.DateField()
    filename = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)


    def saveStatement(self,url,filename):
        
        driver = webdriver.Chrome(ChromeDriverManager().install())                      # use Chrome 
        driver.get(url+filename)
        
        btnJSfunc = "javascript:expand_contract_all(1);"                                # find the following button to expand the content in html
        extendBtn = driver.find_element_by_xpath('//a[@href="'+btnJSfunc+'"]').click()  # click the button
        html = driver.page_source                                                       # got the html source of the page
        driver.close()

        soup = bs(html, 'html.parser')                                                  # use BeeautifulSoup to parse the html 

        date_string  = str(soup.select(".text-title span")[0].string).strip()           # get the date of report
        date = datetime.strptime(date_string, "%B %d, %Y")      
        section = soup.select(".sectionHeadingOpened")                                  # For extracting the section name
        content = soup.select(".sectionContent")                                        # For extracting the content

        _statement = {}   

        for i in range(len(section)):                                                   # forming an dict like:
            _statement[section[i].contents[1]]= content[i]                              # { <report_title> : <untreated html content>}


        obj_Index = {   
            "Net Asset Value" : NetAssetValue,                            
            "Mark-to-Market Performance Summary": MarkToMarketPerformanceSummary,        
            "Realized & Unrealized Performance Summary": RealizedAndUnrealizedPerformanceSummary,
            "Open Positions":OpenPositions,                        
            "Forex Balances":ForexBalances,                   
            "Trades":Trades,                                    
            "Deposits & Withdrawals":DepositsAndWithdrawals,                    
            "Dividends":Dividends,                                
            "Withholding Tax":WithholdingTax,                          
            "Interest Accruals":InterestAccruals,                              
            "Base Currency Exchange Rate": BaseCurrencyExchangeRate,
            # "Cash Report":None,
            # "Complex Positions Summary":None,
            # "Net Stock Position Summary":None,  
            # "Change in Dividend Accruals":None,
            # "Financial Instrument Information": None,
            # "Account Information" :None,
            # "Codes":None,
            # "Notes/Legal Notes":None,
        }

        _dict = {}
        instance = None
        try:
            for key, obj in obj_Index.items():
                if key in _statement :
                    instance = obj()
                    _dict[key] = instance.extraction(_statement[key],date)
                    
                else:
                    continue
        except:
            print(f'error {filename}')
        
        else:
            self.register(date,filename)


    
    def register(self,d,f):
        self.date = d
        self.filename = f
        self.save()



    def __str__(self):
        return self.filename




class Document(models.Model):
    document = models.FileField(upload_to='statement/')
    uploaded_at = models.DateTimeField(default=datetime.now)






def BSString(d):
    return str(d.string).strip()


def BSFloat(d):
    try:
        r = float(str(d.string).replace(",",""))
    except:
        r = 0 
    finally:
        return r