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
class Region:
    def __init__(self,region_id,region_name):
        self.region_id = region_id
        self.region_name = region_name
class Supermarket:
    def __init__(self,supermarket_id,supermarket_name,facility_id):
        self.supermarket_id = supermarket_id
        self.supermarket_name = supermarket_name
        self.facility_id = facility_id
class Item:
    def __init__(self, item_id,facility_id, expiry_date, product_regional_id):
        self.item_id = item_id
        self.facility_id = facility_id
        self.expiry_date = expiry_date
        self.product_regional_id = product_regional_id
class Product:
    def __init__(self, product_regional_id, region_id, sell_price, local_name, order_price, expiry_time, cnt, expired):
        self.product_regional_id = product_regional_id
        self.region_id = region_id
        self.sell_price = sell_price
        self.local_name = local_name
        self.order_price = order_price
        self.expiry_time = expiry_time
        self.cnt = cnt
        self.expired = expired
    def increment(self, supermarket):
        self.cnt += 1
        orderProduct(supermarket, self.product_regional_id, self.expiry_time)
    def decrement(self, supermarket):
        if self.cnt>0:
            self.cnt -= 1
            if self.expired>0:
                self.expired -= 1
            deleteProduct(supermarket,self.product_regional_id)

def clearWindow():
    # Destroy current widgets
    for widget in window.winfo_children():
        widget.destroy()
# Product item manage console
def getItemList(region,supermarket,product):
    dbCursor.execute("SELECT * FROM item WHERE facility_id = " + str(supermarket.facility_id) + " AND product_regional_id = " + str(product.product_regional_id) + ";")
    ret = []
    for item in dbCursor:
        ret.append(Item(item[0],item[1],item[2],item[3]))
    return ret;
def displayProductDetails(region,supermarket,product):
    clearWindow()
    itemList = getItemList(region, supermarket, product)
    if (len(itemList)==0):
        functionStack.pop()
        functionStack.execute()
        return
    # Heading
    label = tk.Label(window, text="Item " + product.local_name + " of supermarket " + supermarket.supermarket_name + " in region " + region.region_name)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Delete oldest
    deleteB = tk.Button(window, text="Delete oldest", command=lambda: (
    deleteProduct(supermarket, product.product_regional_id), displayProductDetails(region, supermarket, product)))
    deleteB.pack()
    # Show item list

    for i in range(len(itemList)):
        prodInfo = tk.Label(window, text = str(i+1) + ") Expiry date: "+str(itemList[i].expiry_date))
        prodInfo.pack()

# Product list manage console
def getMarketProductList(region,supermarket):
    dbCursor.execute("SELECT * FROM product_regional WHERE product_regional_id IN (SELECT product_regional_id FROM item WHERE facility_id = " + str(supermarket.facility_id) + ");")
    ret = []
    for product in dbCursor:
        ret.append(Product(product[0],product[1],product[2],product[3],product[4],product[5],0,0))
    for i in range(len(ret)):
        dbCursor.execute("SELECT COUNT(*) FROM item WHERE facility_id = " + str(supermarket.facility_id) + " AND product_regional_id = " + str(ret[i].product_regional_id)+";")
        ret[i].cnt = int(str(dbCursor.fetchall()[0][0]))
        dbCursor.execute("SELECT COUNT(*) FROM item WHERE facility_id = " + str(
            supermarket.facility_id) + " AND product_regional_id = " + str(
            ret[i].product_regional_id) + " AND item.expiry_date > '" + curDate + "';")
        ret[i].expired = int(str(dbCursor.fetchall()[0][0]))

    return ret
def deleteProduct(supermarket, product_regional_id):
    dbCursor.execute("WITH min_expiry_date AS ( SELECT MIN(expiry_date) AS min_expiry FROM item WHERE facility_id = " + str(supermarket.facility_id) + " AND product_regional_id = " + str(product_regional_id) + ") SELECT item_id FROM item WHERE facility_id = " + str(supermarket.facility_id) + "  AND expiry_date = (SELECT min_expiry FROM min_expiry_date);")
    dbCursor.execute("DELETE FROM item WHERE item_id = " + str(dbCursor.fetchall()[0][0]))
def orderProduct(supermarket, product_regional_id, expiry_time):
    # find max item_id
    dbCursor.execute("SELECT item_id FROM item ORDER BY item_id DESC LIMIT 1;")
    mxId = int(dbCursor.fetchall()[0][0])
    dbCursor.execute("INSERT INTO item (item_id, facility_id, expiry_date, product_regional_id) VALUES (" + str(mxId+1) + ", " + str(supermarket.facility_id) + ", '" + curDate + " + " + str(expiry_time) + "', " + str(product_regional_id) + ");")

def addProductType(region,local_name, sell_price, order_price, expiry_time):
    # find max product_regional_id
    dbCursor.execute("SELECT product_regional_id FROM product_regional ORDER BY product_regional_id DESC LIMIT 1;")
    mxId = int(dbCursor.fetchall()[0][0])
    dbCursor.execute("INSERT INTO product_regional (region_id,sell_price,local_name,order_price,expiry_time,product_regional_id) VALUES ("+
                     str(region.region_id) + "," + sell_price + ",'" + local_name + "'," + order_price + "," + expiry_time + "," + str(mxId+1) + ");")
def createProduct(region,supermarket,productName):
    subWindow = tk.Tk()

    label = tk.Label(subWindow,text="Create new product " + productName)
    label.pack()
    sell_priceL = tk.Label(subWindow, text = "sell price")
    sell_priceL.pack()
    sell_priceE = tk.Entry(subWindow)
    sell_priceE.pack()
    order_priceL = tk.Label(subWindow, text = "order price")
    order_priceL.pack()
    order_priceE = tk.Entry(subWindow)
    order_priceE.pack()
    expiry_timeL = tk.Label(subWindow,text = "expiry time")
    expiry_timeL.pack()
    expiry_timeE = tk.Entry(subWindow)
    expiry_timeE.pack()

    submitB = tk.Button(subWindow,text = "submit", command=lambda:(addProductType(region,productName,sell_priceE.get(),
                                                                          order_priceE.get(),
                                                                          expiry_timeE.get()),subWindow.destroy()))
    submitB.pack()
    subWindow.mainloop()

def addProduct(region, supermarket, productName):
    # find regional_product_id
    dbCursor.execute("SELECT product_regional_id, expiry_time FROM product_regional WHERE local_name = '" + productName + "' AND region_id = " + str(region.region_id)+";")
    cpy = dbCursor.fetchall()
    if len(cpy)==0 or len(cpy[0])==0:
        createProduct(region,supermarket,productName)
        return
    else:
        product_regional_id = int(cpy[0][0])
        expiry_time = int(cpy[0][1])
    orderProduct(supermarket, product_regional_id,expiry_time)

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
        increment = tk.Button(window, text = "+", command=lambda i=i:(productList[i].increment(supermarket),
                                                                      Qcnt[i].config(text="quantity: "+str(productList[i].cnt)),
                                                                      Ecnt[i].config(text="expired: "+str(productList[i].expired))))
        increment.pack()
        decrement = tk.Button(window, text="-", command=lambda i=i: (
        productList[i].decrement(supermarket),
                                                                      Qcnt[i].config(text="quantity: "+str(productList[i].cnt)),
                                                                      Ecnt[i].config(text="expired: "+str(productList[i].expired))))
        decrement.pack()
        detailsB = tk.Button(window, text = "details", command = lambda region = region,supermarket = supermarket,product=productList[i] :(functionStack.add_function(displayProductDetails,region,supermarket,product),displayProductDetails(region,supermarket,product)))
        detailsB.pack()
    # Add product
    addProductLabel = tk.Label(window, text="Type new product name")
    addProductLabel.pack()
    productNameField = tk.Entry(window)
    productNameField.pack()
    addProductB = tk.Button(window, text="Add product",
                                command=lambda: (
                                addProduct(region, supermarket, productNameField.get()), displayProductList(region,supermarket)))
    addProductB.pack()

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

def addSupermarket(region,supermarketName, facility_id=-1):
    # find suitable facility
    if facility_id == -1:
        dbCursor.execute("SELECT facility_id FROM facility WHERE region_id = "+str(region.region_id)+";")
        facility_id = int(dbCursor.fetchall()[0][0])
    # find max supermarket_id
    dbCursor.execute("SELECT supermarket_id FROM supermarket ORDER BY supermarket_id DESC LIMIT 1;")
    mxId = int(dbCursor.fetchall()[0][0])
    print("INSERT INTO supermarket (supermarket_id, supermarket_name, facility_id) VALUES (" + str(mxId + 1) + ", '" + supermarketName + "', "+str(facility_id)+");")
    dbCursor.execute("INSERT INTO supermarket (supermarket_id, supermarket_name, facility_id) VALUES (" + str(mxId + 1) + ", '" + supermarketName + "', "+str(facility_id)+");")
def deleteSupermarket(supermarket):
    dbCursor.execute("DELETE FROM supermarket WHERE supermarket_id="+str(supermarket.supermarket_id))
def displaySupermarketRegion(region):
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
        deleteB = tk.Button(window,text = "delete", command = lambda supermarket = supermarket: (deleteSupermarket(supermarket),displaySupermarketRegion(region)))
        deleteB.pack(side=tk.RIGHT)

    # Add supermarket
    addSupermarketLabel = tk.Label(window, text="Type new supermarket name")
    addSupermarketLabel.pack()
    supermarketNameField = tk.Entry(window)
    supermarketNameField.pack()
    addSupermarketB = tk.Button(window, text="Add supermarket",
                           command=lambda: (addSupermarket(region,supermarketNameField.get()), displaySupermarketRegion(region)))
    addSupermarketB.pack()

# Marker region selector
def getMarketRegions():
    dbCursor.execute("SELECT region_id,region_name FROM region;")
    ret = []
    for region in dbCursor:
        ret.append(Region(region[0],region[1]))
    return ret

def addRegion(regionName):
    # find max region_id
    dbCursor.execute("SELECT region_id FROM region ORDER BY region_id DESC LIMIT 1;")
    mxId = int(dbCursor.fetchall()[0][0])
    newRegion = mxId+1
    dbCursor.execute("INSERT INTO region (region_id, region_name, road_list_id) VALUES ("+str(mxId+1)+", '" + regionName + "', 1);")
    # find max facility_id
    dbCursor.execute("SELECT facility_id FROM facility ORDER BY facility_id DESC LIMIT 1;")
    mxId = int(dbCursor.fetchall()[0][0])
    dbCursor.execute("INSERT INTO facility (facility_id, region_id) VALUES (" + str(mxId+1) + ", " + str(newRegion) + ");")
def displayRegionSelector():
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
        regionB = tk.Button(window, text = region.region_name, command = lambda region = region: (functionStack.add_function(displaySupermarketRegion,region),displaySupermarketRegion(region)))
        regionB.pack()
    # Add region
    addRegionLabel = tk.Label(window, text = "Type new region name")
    addRegionLabel.pack()
    regionNameField = tk.Entry(window)
    regionNameField.pack()
    addRegionB = tk.Button(window, text = "Add region", command = lambda: (addRegion(regionNameField.get()),displayRegionSelector()))
    addRegionB.pack()

# Main screen
def displayMainScreen():
    clearWindow()
    # Heading
    label = tk.Label(window, text="Story management system")
    label.pack()
    # Supermarket management
    marketB = tk.Button(window, text="Start", command=lambda: (functionStack.add_function(displayRegionSelector),displayRegionSelector()))
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
conn.autocommit = True
dbCursor = conn.cursor()
#test()

window = tk.Tk()
functionStack = FunctionStack()
functionStack.add_function(displayMainScreen)
displayMainScreen()
window.mainloop()

dbCursor.close()
