import tkinter as tk
import psycopg2

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

class Region:
    def __init__(self,region_id,region_name):
        self.region_id = region_id
        self.region_name = region_name
class Supermarket:
    def __init__(self,supermarket_id,supermarket_name,facility_id):
        self.supermarket_id = supermarket_id
        self.supermarket_name = supermarket_name
        self.facility_id = facility_id

class Product:
    def __init__(self, product_regional_id, region_id, product_id, sell_price, local_name, order_price, expiry_time, cnt, expired):
        self.product_regional_id = product_regional_id
        self.region_id = region_id
        self.product_id = product_id
        self.sell_price = sell_price
        self.local_name = local_name
        self.order_price = order_price
        self.expiry_time = expiry_time
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
def getMarketProductList(region,supermarket):
    dbCursor.execute("SELECT * FROM product_regional WHERE product_regional_id IN (SELECT product_regional_id FROM item WHERE facility_id = " + str(supermarket.facility_id) + ");")
    ret = []
    for product in dbCursor:
        ret.append(Product(product[0],product[1],product[2],product[3],product[4],product[5],product[6],0,0))
    for i in range(len(ret)):
        dbCursor.execute("SELECT COUNT(*) FROM item WHERE facility_id = " + str(supermarket.facility_id) + " AND product_regional_id = " + str(ret[i].product_regional_id)+";")
        ret[i].cnt = int(str(dbCursor.fetchall()[0][0]))
        dbCursor.execute("SELECT COUNT(*) FROM item WHERE facility_id = " + str(
            supermarket.facility_id) + " AND product_regional_id = " + str(
            ret[i].product_regional_id) + " AND item.creation_date + " + str(ret[i].expiry_time) + "> '" + curDate + "';")
        ret[i].expired = int(str(dbCursor.fetchall()[0][0]))

    return ret
def displayProductList(region,supermarket):
    clearWindow()
    # Heading
    label = tk.Label(window, text = "Products of "+supermarket.supermarket_name + " in region " + region.region_name)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Display product list
    productList = getMarketProductList(region,supermarket)
    Qcnt = []
    Ecnt = []
    for i in range(len(productList)):
        productLabel = tk.Label(window, text = "Name "+productList[i].local_name)
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
        detailsB = tk.Button(window, text = "details", command = lambda region = region,supermarket = supermarket,product=productList[i] :(functionStack.add_function(displayProductDetails,region,supermarket,product),displayProductDetails(region,supermarket,product)))
        detailsB.pack()


# Supermarket manage console
def displayMarket(region,supermarket):
    clearWindow()
    # Heading
    label = tk.Label(window, text = "Management console of "+supermarket.supermarket_name + " in region " + region.region_name)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Go to product list
    productListB = tk.Button(window, text = "Product list", command = (lambda region = region,supermarket = supermarket: (functionStack.add_function(displayProductList,region,supermarket),displayProductList(region,supermarket))))
    productListB.pack()

# Supermarket selector
def getSupermarketList(region):
    dbCursor.execute("SELECT s.* FROM supermarket s INNER JOIN facility f ON s.facility_id = f.facility_id WHERE f.region_id = " + str(region.region_id)+";")
    ret = []
    for supermarket in dbCursor:
        ret.append(Supermarket(supermarket[0],supermarket[1],supermarket[2]))
    return ret
def displayMarketRegion(region):
    clearWindow()
    # Heading
    label = tk.Label(window, text="Supermarkets in region " + region.region_name)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Display list of markets
    supermarketList = getSupermarketList(region)

    for supermarket in supermarketList:
        marketB = tk.Button(window, text = supermarket.supermarket_name, command = lambda region=region, supermarket=supermarket: (functionStack.add_function(displayMarket,region,supermarket),displayMarket(region,supermarket)))
        marketB.pack()

# Marker region selector
def getMarketRegions():
    dbCursor.execute("SELECT region_id,region_name FROM region;")
    ret = []
    for region in dbCursor:
        ret.append(Region(region[0],region[1]))
    return ret

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
        regionB = tk.Button(window, text = region.region_name, command = lambda region = region: (functionStack.add_function(displayMarketRegion,region),displayMarketRegion(region)))
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
def test():
    getSupermarketList(Region(1,"sdfs"))
    i = 1
    while i < 2:
        i = 1
curDate = "2023-01-07"
conn = psycopg2.connect(database="postgres", user="admin",
    password="", host="localhost", port=5432)
dbCursor = conn.cursor()
#test()

window = tk.Tk()
functionStack = FunctionStack()
functionStack.add_function(displayMainScreen)
displayMainScreen()
window.mainloop()
