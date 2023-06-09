import tkinter as tk
import psycopg2
import matplotlib.pyplot as plt
import datetime
import numpy as np
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
    def __init__(self, product_regional_id, region_id, sell_price, local_name, order_price, expiry_time, cnt=0, expired=0):
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
    return ret
def sellItem(supermarket,item,date):
    # calculate price
    dbCursor.execute("SELECT sell_price FROM product_regional WHERE product_regional_id = " + str(item.product_regional_id))
    price = dbCursor.fetchall()[0][0]
    # add to sales_history
    dbCursor.execute("INSERT INTO sales_history (item_id, price, date, supermarket_id) VALUES (%s, %s, %s, %s);",
                     (item.product_regional_id,price,date,supermarket.supermarket_id))
    dbCursor.execute("INSERT INTO sold_items (item_id, product_regional_id, sell_price, sell_date) VALUES (%s, %s, %s, %s);",
                     (item.item_id,item.product_regional_id,price,date))
    dbCursor.execute("DELETE FROM item WHERE item_id = " + str(item.item_id))
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
        # buy button
        buyB = tk.Button(window,text = "Bought",command=lambda i=i:(sellItem(supermarket,itemList[i],curDate),
                         displayProductDetails(region,supermarket,product)))
        buyB.pack()

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

def getMarketWorkersList(region,supermarket):
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

def addOrderHistory(facility_id, order_price, order_date):
    # find max order_id
    dbCursor.execute("SELECT order_id FROM order_history ORDER BY order_id DESC LIMIT 1;")
    result = dbCursor.fetchall()
    if result:
        mxId = int(result[0][0])
    else:
        mxId = 0
    dbCursor.execute("INSERT INTO order_history (order_id,facility_id,buy_price,order_date) VALUES (%s, %s, %s, %s);",
                     (mxId+1,facility_id,order_price,order_date))
    return mxId+1

def addDeliveryHistory(supermarket,order_id,delivery_date):
    # find max delivery_id
    dbCursor.execute("SELECT delivery_id FROM deliveries_history ORDER BY delivery_id DESC LIMIT 1;")
    result = dbCursor.fetchall()
    if result:
        mxId = int(result[0][0])
    else:
        mxId = 0
    dbCursor.execute("INSERT INTO deliveries_history (delivery_id,supermarket_id,order_id,delivery_date) VALUES (%s, %s, %s, %s);",
                     (mxId + 1, supermarket.supermarket_id, order_id, delivery_date))
def orderProduct(supermarket, product_regional_id, expiry_time):
    # find max item_id
    dbCursor.execute("SELECT item_id FROM item ORDER BY item_id DESC LIMIT 1;")
    result = dbCursor.fetchall()
    if result:
        mxId = int(result[0][0])
    else:
        mxId = 0
    dbCursor.execute("INSERT INTO item (item_id, facility_id, expiry_date, product_regional_id) VALUES (" + str(mxId+1) + ", " + str(supermarket.facility_id) + ", '" + curDate + " + " + str(expiry_time) + "', " + str(product_regional_id) + ");")
    # get order price
    dbCursor.execute("SELECT order_price FROM product_regional WHERE product_regional_id = " + str(product_regional_id))
    order_price = int(dbCursor.fetchall()[0][0])
    order_id = addOrderHistory(supermarket.facility_id,order_price,curDate)
    # add to deliveries history
    addDeliveryHistory(supermarket,order_id,curDate)

def addProductType(region,local_name, sell_price, order_price, expiry_time):
    # find max product_regional_id
    dbCursor.execute("SELECT product_regional_id FROM product_regional ORDER BY product_regional_id DESC LIMIT 1;")
    result = dbCursor.fetchall()
    if result:
        mxId = int(result[0][0])
    else:
        mxId = 0
    dbCursor.execute("INSERT INTO product_regional (region_id,sell_price,local_name,order_price,expiry_time,product_regional_id) VALUES ("+
                     str(region.region_id) + "," + sell_price + ",'" + local_name + "'," + order_price + "," + expiry_time + "," + str(mxId+1) + ");")
    addPriceChange(Product(mxId, region.region_id, sell_price, local_name, order_price, expiry_time), order_price)
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

def displayStuffList(region,supermarket):
    clearWindow()
    # Heading
    label = tk.Label(window, text = "Workers of "+supermarket.supermarket_name + " in region " + region.region_name)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Display workers list
    peopleList = getMarketWorkersList(region,supermarket)
    Qcnt = []
    Ecnt = []
    for i in range(len(peopleList)):
        workerLabel = tk.Label(window, text = "First Name "+workersList[i].first_name)
        WorkerLabel.pack()
        workerLabel = tk.Label(window, text="Second Name " + workersList[i].second_name)
        WorkerLabel.pack()
        workerLabel = tk.Label(window, text="Position Name" + workersList[i].position_name)
        WorkerLabel.pack()
        decrement.pack()
        detailsB = tk.Button(window, text = "History", command = lambda region = region,supermarket = supermarket,worker=workersList[i] :(functionStack.add_function(displayHistoryOfWorkDetails,region,supermarket,worker),displayHistoryOfWorkDetails(region,supermarket,worker)))
        detailsB.pack()
    # Add worker
    addWorkerLabel = tk.Label(window, text="Type new worker first name")
    addWorkerLabel.pack()
    WorkerNameField = tk.Entry(window)
    WorkerNameField.pack()
    addWorkerLabel1 = tk.Label(window, text="Type new worker last name")
    addWorkerLabel1.pack()
    WorkerNameField1 = tk.Entry(window)
    WorkerNameField1.pack()
    addWorkerB = tk.Button(window, text="Add worker",
                                command=lambda: (
                                addWorker(region, supermarket, WorkerNameField.get(), WorkerNameField1.get()), displayProductList(region,supermarket)))
    addWorkerB.pack()

# Supermarket manage console

def getMarketOrders(supermarket):
    dbCursor.execute("SELECT * FROM deliveries_history WHERE supermarket_id = " + str(supermarket.supermarket_id))
    deliveries = []
    for delivery in dbCursor:
        deliveries.append([delivery[3],delivery[1]])
    ret = []
    for [order_id,date] in deliveries:
        dbCursor.execute("SELECT * FROM order_history WHERE order_id = " + str(order_id))
        cpy = dbCursor.fetchall()
        ret.append([date,cpy[0][1]])
    return ret
def getMarketSales(supermarket):
    dbCursor.execute("SELECT * FROM sales_history WHERE supermarket_id = " + str(supermarket.supermarket_id))
    ret = []
    for sale in dbCursor:
        ret.append([sale[2],sale[1]])
    return ret
def displayMarketProfit(supermarket):
    orders = getMarketOrders(supermarket)
    sales = getMarketSales(supermarket)
    dataPoints = []
    for point in orders:
        dataPoints.append([point[0],-point[1]])
    for point in sales:
        dataPoints.append(point)
    dataPoints.sort()
    dates = []
    y_values = []
    for point in dataPoints:
        dates.append(point[0])
        y_values.append(point[1])
    # Convert string dates to datetime objects
    x = [datetime.datetime.strptime(str(date), '%Y-%m-%d') for date in dates]

    # Compute cumulative sum of y
    y = np.cumsum(y_values)

    # Plot y versus x as lines and/or markers
    plt.plot(x, y)

    # Set the x and y axis labels
    plt.xlabel('Date')
    plt.ylabel('Cumulative y')

    # Set the title of the graph
    plt.title('My Graph')

    # Format x-axis to display dates in a particular format
    plt.gcf().autofmt_xdate()

    # Display the figure
    plt.show()
def displayMarket(region,supermarket):
    clearWindow()
    # Heading
    label = tk.Label(window, text = "Management console of "+supermarket.supermarket_name + " in region " + region.region_name)
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Profit graph
    profitGraphB = tk.Button(window, text="Display market profit", command=lambda: displayMarketProfit(supermarket))
    profitGraphB.pack()
    # Go to product list
    productListB = tk.Button(window, text = "Product list", command = (lambda region = region,supermarket = supermarket: (functionStack.add_function(displayProductList,region,supermarket),displayProductList(region,supermarket))))
    productListB.pack()
    # Go to workers list
    workersListB = tk.Button(window, text="People list", command=(lambda region=region, supermarket=supermarket: (
    functionStack.add_function(displayStuffList, region, supermarket), displayStuffList(region, supermarket))))
    workersListB.pack()

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
    result = dbCursor.fetchall()
    if result:
        mxId = int(result[0][0])
    else:
        mxId = 0
    print("INSERT INTO supermarket (supermarket_id, supermarket_name, facility_id) VALUES (" + str(mxId + 1) + ", '" + supermarketName + "', "+str(facility_id)+");")
    dbCursor.execute("INSERT INTO supermarket (supermarket_id, supermarket_name, facility_id) VALUES (" + str(mxId + 1) + ", '" + supermarketName + "', "+str(facility_id)+");")
def deleteSupermarket(supermarket):
    dbCursor.execute("DELETE FROM supermarket WHERE supermarket_id="+str(supermarket.supermarket_id))
def deleteRegion(region):
    dbCursor.execute("DELETE FROM region WHERE region_id="+str(region.region_id))
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
        deleteB.pack()

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
    result = dbCursor.fetchall()
    if result:
        mxId = int(result[0][0])
    else:
        mxId = 0

    newRegion = mxId + 1
    dbCursor.execute("INSERT INTO region (region_id, region_name, road_list_id) VALUES (%s, %s, 1);", (newRegion, regionName))

    # find max facility_id
    dbCursor.execute("SELECT facility_id FROM facility ORDER BY facility_id DESC LIMIT 1;")
    result = dbCursor.fetchall()
    if result:
        mxId = int(result[0][0])
    else:
        mxId = 0

    dbCursor.execute("INSERT INTO facility (facility_id, region_id) VALUES (%s, %s);", (mxId + 1, newRegion))
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
        deleteB = tk.Button(window, text="delete", command=lambda region=region: (
        deleteRegion(region), displayRegionSelector()))
        deleteB.pack()
    # Add region
    addRegionLabel = tk.Label(window, text = "Type new region name")
    addRegionLabel.pack()
    regionNameField = tk.Entry(window)
    regionNameField.pack()
    addRegionB = tk.Button(window, text = "Add region", command = lambda: (addRegion(regionNameField.get()),displayRegionSelector()))
    addRegionB.pack()
# Product control
def getProductList():
    dbCursor.execute("SELECT * FROM product_regional;")
    ret = []
    for product in dbCursor:
        ret.append(Product(product[0], product[1],product[2],product[3],product[4],product[5],0,0))
    return ret

def addPriceChange(product,new_price):
    # find max price_change_id
    dbCursor.execute("SELECT price_change_id FROM price_change ORDER BY price_change_id DESC LIMIT 1;")
    result = dbCursor.fetchall()
    if result:
        mxId = int(result[0][0])
    else:
        mxId = 0

    newPriceChange = mxId + 1
    dbCursor.execute("INSERT INTO price_change (price_change_id, product_regional_id, new_price,old_price,date) VALUES (%s, %s, %s, %s, %s);",
                     (newPriceChange,product.product_regional_id,new_price,product.order_price,curDate))


def changeData(product, local_name,sell_price,order_price,expiry_time):
    if product.local_name!=local_name:
        dbCursor.execute("UPDATE product_regional SET local_name = '" + str(local_name) +
                         "' WHERE product_regional_id="+str(product.product_regional_id) + ";")
    if str(product.sell_price)!=sell_price:
        dbCursor.execute("UPDATE product_regional SET sell_price = '" + str(sell_price) +
                         "' WHERE product_regional_id=" + str(product.product_regional_id) + ";")
    if str(product.order_price) != order_price:
        dbCursor.execute("UPDATE product_regional SET order_price = '" + str(order_price) +
                         "' WHERE product_regional_id=" + str(product.product_regional_id) + ";")
        addPriceChange(product,order_price)
    if str(product.expiry_time) != expiry_time:
        dbCursor.execute("UPDATE product_regional SET expiry_time = '" + str(expiry_time) +
                         "' WHERE product_regional_id=" + str(product.product_regional_id) + ";")

def getProductDataPoints(product):
        dbCursor.execute("SELECT * FROM price_change WHERE product_regional_id = " + str(product.product_regional_id) + "ORDER BY date;")
        ret = []
        for priceChange in dbCursor:
            ret.append([priceChange[3],int(priceChange[2])])
        return ret
def displayPriceGraph(product):
    dataPoints = getProductDataPoints(product)
    dates = []
    y = []
    for point in dataPoints:
        dates.append(point[0])
        y.append(point[1])
    # Convert string dates to datetime objects
    x = [datetime.datetime.strptime(str(date), '%Y-%m-%d') for date in dates]

    # Plot y versus x as lines and/or markers
    plt.plot(x, y)

    # Set the x and y axis labels
    plt.xlabel('Date')
    plt.ylabel('y-axis')

    # Set the title of the graph
    plt.title('My Graph')

    # Format x-axis to display dates in a particular format
    plt.gcf().autofmt_xdate()

    # Display the figure
    plt.show()
def editProdInfo(product):
    curWindow = tk.Tk()
    displayGraphB = tk.Button(curWindow,text = "Display price history",command=lambda :(displayPriceGraph(product)))
    displayGraphB.pack()
    label = tk.Label(curWindow,text = "Edit info")
    label.pack()
    #Name
    nameL = tk.Label(curWindow,text = "Name")
    nameL.pack()
    nameE = tk.Entry(curWindow)
    nameE.pack()
    nameE.insert(0,product.local_name)
    #Sell
    sellL = tk.Label(curWindow,text = "Sell price")
    sellL.pack()
    sellE = tk.Entry(curWindow)
    sellE.pack()
    sellE.insert(0,str(product.sell_price))
    #Order
    orderL = tk.Label(curWindow,text = "Order price")
    orderL.pack()
    orderE = tk.Entry(curWindow)
    orderE.pack()
    orderE.insert(0,str(product.order_price))
    #Expiry
    expiryL = tk.Label(curWindow,text = "Expiry time")
    expiryL.pack()
    expiryE = tk.Entry(curWindow)
    expiryE.pack()
    expiryE.insert(0,str(product.expiry_time))
    #Submit
    submitB = tk.Button(curWindow, text="Submit",
                           command=lambda: (changeData(product, nameE.get(),sellE.get(),orderE.get(),expiryE.get()),curWindow.destroy(),displayProductControl()))
    submitB.pack()
    curWindow.mainloop()

def displayProductControl():
    clearWindow()
    # Heading
    label = tk.Label(window, text="Product control")
    label.pack()
    # Go back
    backB = tk.Button(window, text="Back", command=lambda: (functionStack.pop(), functionStack.execute()))
    backB.pack()
    # Product list
    productList = getProductList()
    regionList = getMarketRegions()
    regionDict = {}
    for region in regionList:
        regionDict[region.region_id] = region.region_name
    for product in productList:
        productB = tk.Button(window,text = product.local_name + "  " +
                                           regionDict[product.region_id] + ": sell price: "+str(product.sell_price) +
                                           ", order price: "+str(product.order_price) + ", expiry time: "
                                           + str(product.expiry_time),
                             command = lambda product = product: (editProdInfo(product)))
        productB.pack()


# Main screen
def displayMainScreen():
    clearWindow()
    # Heading
    label = tk.Label(window, text="Story management system")
    label.pack()
    # Supermarket management
    marketB = tk.Button(window, text="Supermarkets", command=lambda: (functionStack.add_function(displayRegionSelector),displayRegionSelector()))
    marketB.pack()
    # Product management
    pricesB = tk.Button(window, text="Products", command=lambda:(functionStack.add_function(displayProductControl),displayProductControl()))
    pricesB.pack()

curDate = "2023-01-07"
conn = psycopg2.connect(database="postgres", user="admin",
    password="", host="localhost", port=5432)
conn.autocommit = True
dbCursor = conn.cursor()

window = tk.Tk()
functionStack = FunctionStack()
functionStack.add_function(displayMainScreen)
displayMainScreen()
window.mainloop()

dbCursor.close()

