import tkinter as tk
#import pyodbc

class FunctionStack:
    def __init__(self):
        self.stack = []
        self.sz = 0

    def add_function(self, func, *args, **kwargs):
        self.stack.append((func, args, kwargs))
        self.sz += 1
    def execute(self):
        func, args, kwargs = self.stack[self.sz-1]
        func(*args, **kwargs)
    def pop(self):
        self.stack.pop()
        self.sz -= 1
class Item:
    def __init__(self,creationDate):
        self.creationDate = creationDate

class Product:
    def __init__(self, id, name, storagePeriod, cnt, expired):
        self.id = id
        self.name = name
        self.storagePeriod = storagePeriod
        self.cnt = cnt
        self.expired = expired
    def increment(self):
        self.cnt += 1
    def decrement(self):
        if self.cnt>0:
            self.cnt -= 1
            if self.expired>0:
                self.expired -= 1
def clearWindow():
    # Destroy current widgets
    for widget in window.winfo_children():
        widget.destroy()
# Product item manage console
def getItemList(regionName,marketName,productName):
    return [Item(45),Item(88),Item(26)]
def displayProductDetails(regionName,marketName,productName):
    clearWindow()
    # Heading
    label = tk.Label(window, text="Item " + productName + " of supermarket " + marketName + " in region " + regionName)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Show item list
    itemList = getItemList(regionName,marketName,productName)
    for i in range(len(itemList)):
        prodInfo = tk.Label(window, text = "Creation date: "+str(itemList[i].creationDate))
        prodInfo.pack()

# Product list manage console
def getMarketProductList(regionName,marketName):
    return [Product(0,"apple "+marketName, 25,4,3), Product(1,"banana "+marketName, 13,5,7)]
def displayProductList(regionName,marketName):
    clearWindow()
    # Heading
    label = tk.Label(window, text = "Products of "+marketName + " in region " + regionName)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Display product list
    productList = getMarketProductList(regionName,marketName)
    Qcnt = []
    Ecnt = []
    for i in range(len(productList)):
        productLabel = tk.Label(window, text = "Name "+productList[i].name)
        productLabel.pack()

        Qcnt.append(tk.Label(window, text = "quantity: "+str(productList[i].cnt)))
        Qcnt[i].pack()
        Ecnt.append(tk.Label(window, text = "expired: "+str(productList[i].expired)))
        Ecnt[i].pack()
        increment = tk.Button(window, text = "+", command=lambda i=i:(productList[i].increment(),
                                                                      Qcnt[i].config(text="quantity: "+str(productList[i].cnt)),
                                                                      Ecnt[i].config(text="expired: "+str(productList[i].expired))))
        increment.pack()
        decrement = tk.Button(window, text="-", command=lambda i=i: (
        productList[i].decrement(),
                                                                      Qcnt[i].config(text="quantity: "+str(productList[i].cnt)),
                                                                      Ecnt[i].config(text="expired: "+str(productList[i].expired))))
        decrement.pack()
        detailsB = tk.Button(window, text = "details", command = lambda regionName = regionName,marketName = marketName,productName=productList[i].name :(functionStack.add_function(displayProductDetails,regionName,marketName,productName),displayProductDetails(regionName,marketName,productName)))
        detailsB.pack()


# Supermarket manage console
def displayMarket(regionName,marketName):
    clearWindow()
    # Heading
    label = tk.Label(window, text = "Management console of "+marketName + " in region " + regionName)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Go to product list
    productListB = tk.Button(window, text = "Product list", command = (lambda regionName = regionName,marketName = marketName: (functionStack.add_function(displayProductList,regionName,marketName),displayProductList(regionName,marketName))))
    productListB.pack()

# Supermarket selector
def getMarketList(regionName):
    return ["M1 "+regionName, "M2 "+regionName, "M3 "+regionName]
def displayMarketRegion(regionName):
    clearWindow()
    # Heading
    label = tk.Label(window, text="Supermarkets in region " + regionName)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Display list of markets
    marketList = getMarketList(regionName)

    for market in marketList:
        marketB = tk.Button(window, text = market, command = lambda regionName = regionName, marketName=market: (functionStack.add_function(displayMarket,regionName,marketName),displayMarket(regionName,marketName)))
        marketB.pack()

# Marker region selector
def getMarketRegions():
    return ["My mum", "your mum", "our mum"]

def displayMarketRegionSelector():
    clearWindow()
    # Heading
    label = tk.Label(window, text="Choose region")
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Display list of regions
    regionList = getMarketRegions()

    for region in regionList:
        regionB = tk.Button(window, text = region, command = lambda regionName=region: (functionStack.add_function(displayMarketRegion,regionName),displayMarketRegion(regionName)))
        regionB.pack()

# Main screen
def displayMainScreen():
    clearWindow()
    # Heading
    label = tk.Label(window, text="What do you want do handle?")
    label.pack()
    # Supermarket management
    marketB = tk.Button(window, text="Supermarkets", command=lambda: (functionStack.add_function(displayMarketRegionSelector),displayMarketRegionSelector()))
    marketB.pack()
    # Prices management
    #pricesB = tk.Button(window, text="Prices", command=on_prices_click())
    #pricesB.pack()

#fix this part
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password')

window = tk.Tk()
functionStack = FunctionStack()
functionStack.add_function(displayMainScreen)
displayMainScreen()
window.mainloop()
