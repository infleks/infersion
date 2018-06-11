from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# Create your views here.


def display(request):   
    data = []

    cuss = CustomerInfo.objects.all()
    for c in cuss:
        tempDict = {}
        tempDict['cus'] = c

        tempDict['prodMan'] = ProductManagerHistory.objects.filter(customer=c)
        tempDict['techMan'] = TechnicalManagerHistory.objects.filter(
            customer=c)

        if len(tempDict['prodMan']) > 0:
            tempDict['prodMan'] = tempDict['prodMan'][len(
                tempDict['prodMan'])-1]

        if len(tempDict['techMan']) > 0:
            tempDict['techMan'] = tempDict['techMan'][len(
                tempDict['techMan'])-1]

        tempHist = ProductHistory.objects.filter(customer=c)
        tempDict['prodHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['prodHist']:
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['prodHist'][t.productversion.productmodule.pk].prodInstallationTime) > str(t.prodInstallationTime):
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

        tempHist = TestProductHistory.objects.filter(customer=c)
        tempDict['testProdHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['testProdHist']:
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['testProdHist'][t.productversion.productmodule.pk].testInstallationTime) > str(t.testInstallationTime):
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t

        data.append(tempDict)

    return render(request, 'display.html', {'data': data})


def manage(request):
    
    data = []

    cuss = CustomerInfo.objects.all()
    for c in cuss:
        tempDict = {}
        tempDict['cus'] = c

        tempDict['prodMan'] = ProductManagerHistory.objects.filter(customer=c)
        tempDict['techMan'] = TechnicalManagerHistory.objects.filter(
            customer=c)

        if len(tempDict['prodMan']) > 0:
            tempDict['prodMan'] = tempDict['prodMan'][len(
                tempDict['prodMan'])-1]

        if len(tempDict['techMan']) > 0:
            tempDict['techMan'] = tempDict['techMan'][len(
                tempDict['techMan'])-1]

        tempHist = ProductHistory.objects.filter(customer=c)
        tempDict['prodHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['prodHist']:
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['prodHist'][t.productversion.productmodule.pk].prodInstallationTime) > str(t.prodInstallationTime):
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

        tempHist = TestProductHistory.objects.filter(customer=c)
        tempDict['testProdHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['testProdHist']:
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['testProdHist'][t.productversion.productmodule.pk].testInstallationTime) > str(t.testInstallationTime):
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t
        
        data.append(tempDict)
        dataToSend = {
            'cus': CustomerInfo.objects.all(),
            'prodMan': ProductManagerHistory.objects.all(),
            'techMan': TechnicalManagerHistory.objects.all(),
            'db': DatabaseInfo.objects.all(),
            'dbHis': DatabaseVersion.objects.all(),
            'server': ServerInfo.objects.all(),
            'svHis': ServerVersion.objects.all(),
            'prod': ProductInfo.objects.all(),
            'prodMod': ProductModule.objects.all(),
            'prodVer': ProductVersion.objects.all(),
            'prodLoadTime': ProductHistory.objects.all(),
            'testLoadTime': TestProductHistory.objects.all(),
            'infHis': InfinaWorkerHistory.objects.all(),
            'data' : data
    }

    return render(request, 'add.html', dataToSend)

def add(request):
    if(request.method == 'POST'):
        p = request.POST
        if p['add_what'] == "cus":
            c = CustomerInfo()
            c.customerName = p['cus_name']
            c.save()
        elif p['add_what'] == "prodMan":
            pM = ProductManagerHistory()
            pM.customer = CustomerInfo.objects.get(pk=p['cus_id'])
            pM.prodManName = p['prodMan_name']
            pM.prodManEmail = p['prodMan_email']
            pM.prodManPhoneNumber = p['prodMan_phone']
            pM.whenIsProdManResponsible = p['prodMan_date']
            pM.save()
        elif p['add_what'] == "techMan":
            tM = TechnicalManagerHistory()
            tM.customer = CustomerInfo.objects.get(pk=p['cus_id'])
            tM.techManName = p['techMan_name']
            tM.prodManEmail = p['techMan_email']
            tM.techManPhoneNumber = p['techMan_phone']
            tM.whenIsTechManResponsible = p['techMan_date']
            tM.save()
        elif p['add_what'] == "db":
            d = DatabaseInfo()
            d.databaseName = p['db_name']
            d.save()
        elif p['add_what'] == "dbHis":
            dH = DatabaseVersion()
            dH.database = DatabaseInfo.objects.get(pk=p['db_id'])
            dH.databaseVersionName = p['dbVer_name']
            dH.save()
        elif p['add_what'] == "server":
            s = ServerInfo()
            s.serverName = p['server_name']
            s.save()
        elif p['add_what'] == "svHis":
            sH = ServerVersion()
            sH.server = ServerInfo.objects.get(pk=p['sv_id'])
            sH.serverVersionName = p['svVer_name']
            sH.save()
        elif p['add_what'] == 'prod':
            pr = ProductInfo()
            pr.productName = p['prod_name']
            pr.save()
        elif p['add_what'] == 'prodMod':
            prM = ProductModule()
            prM.product = ProductInfo.objects.get(pk=p['prod_id'])
            prM.moduleName = p['prodMod_name']
            prM.save()
        elif p['add_what'] == 'prodVer':
            pV = ProductVersion()
            pV.productmodule = ProductModule.objects.get(pk=p['prodMod_id'])
            pV.productVersionName = p['prodVer_name']
            pV.save()
        elif p['add_what'] == 'prodLoadTime':
            pH = ProductHistory()
            pH.customer = CustomerInfo.objects.get(pk=p['cus_id'])
            pH.productversion = ProductVersion.objects.get(pk=p['prodVers_id'])
            pH.databaseversion = DatabaseVersion.objects.get(pk=p['dbVer_id'])
            pH.serverversion = ServerVersion.objects.get(pk=p['svVer_id'])
            pH.prodInstallationTime = p['prodLoadTime_date']
            pH.save()
        elif p['add_what'] == 'testLoadTime':
            tH = TestProductHistory()
            tH.customer = CustomerInfo.objects.get(pk=p['cus_id'])
            tH.productversion = ProductVersion.objects.get(pk=p['prodVers_id'])
            tH.databaseversion = DatabaseVersion.objects.get(pk=p['dbVer_id'])
            tH.serverversion = ServerVersion.objects.get(pk=p['svVer_id'])
            tH.testInstallationTime = p['testLoadTime_date']
            tH.save()
        elif p['add_what'] == 'infHis':
            iH = InfinaWorkerHistory()
            iH.producthistory = ProductHistory.objects.get(pk=p['prodHis_id'])
            iH.testhistory = TestProductHistory.objects.get(
                pk=p['tprodHis_id'])
            iH.workerName = p['infHis_name']
            iH.workerSurname = p['infHis_surname']
            iH.savingTime = p['infHis_date']
            iH.save()
        
    return redirect('manage')

def detail(request):

    if request.method != "GET":
        return redirect('display')

    if 'id' not in request.GET.keys():
        return redirect('display')

    pk1 = request.GET['id']
    cusData = CustomerInfo.objects.get(pk=pk1)
    prodData= ProductHistory.objects.filter(customer=cusData)
    testData= TestProductHistory.objects.filter(customer=cusData)


    dataToSend = {
        'prodData': prodData,
        'testData': testData
    }

    return render(request, 'detail.html', dataToSend)


def addProdMan(request):
    data = []

    cuss = CustomerInfo.objects.all()
    for c in cuss:
        tempDict = {}
        tempDict['cus'] = c

        tempDict['prodMan'] = ProductManagerHistory.objects.filter(customer=c)
        tempDict['techMan'] = TechnicalManagerHistory.objects.filter(
            customer=c)

        if len(tempDict['prodMan']) > 0:
            tempDict['prodMan'] = tempDict['prodMan'][len(
                tempDict['prodMan'])-1]

        if len(tempDict['techMan']) > 0:
            tempDict['techMan'] = tempDict['techMan'][len(
                tempDict['techMan'])-1]

        tempHist = ProductHistory.objects.filter(customer=c)
        tempDict['prodHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['prodHist']:
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['prodHist'][t.productversion.productmodule.pk].prodInstallationTime) > str(t.prodInstallationTime):
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

        tempHist = TestProductHistory.objects.filter(customer=c)
        tempDict['testProdHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['testProdHist']:
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['testProdHist'][t.productversion.productmodule.pk].testInstallationTime) > str(t.testInstallationTime):
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t
        
        data.append(tempDict)
        dataToSend = {
            'cus': CustomerInfo.objects.all(),
            'prodMan': ProductManagerHistory.objects.all(),
            'techMan': TechnicalManagerHistory.objects.all(),
            'db': DatabaseInfo.objects.all(),
            'dbHis': DatabaseVersion.objects.all(),
            'server': ServerInfo.objects.all(),
            'svHis': ServerVersion.objects.all(),
            'prod': ProductInfo.objects.all(),
            'prodMod': ProductModule.objects.all(),
            'prodVer': ProductVersion.objects.all(),
            'prodLoadTime': ProductHistory.objects.all(),
            'testLoadTime': TestProductHistory.objects.all(),
            'infHis': InfinaWorkerHistory.objects.all(),
            'data' : data
    }

    return render(request, 'adds/productManager.html', dataToSend)



def addCus(request):
    return render(request, 'adds/customerInfo.html')


def addProd(request):
    return render(request, 'adds/productInfo.html')

def addProdMod(request):
    return render(request, 'adds/productModule.html')

def addServer(request):
    return render(request, 'adds/serverInfo.html')

def addProdVer(request):
    prodMod=ProductModule.objects.all()
    dataToSend={
        'prodMod' : prodMod
    }
    return render(request, 'adds/productVersion.html')

def addDbVer(request):
    db=DatabaseInfo.objects.all()
    dataToSend={
        'db' : db
    }
    return render(request, 'adds/databaseVersion.html', dataToSend)
    
def addServerVer(request):
    servers=ServerInfo.objects.all()
    dataToSend={
        'servers' : servers
    }
    return render(request, 'adds/serverVersion.html', dataToSend)

def addDB(request):
    return render(request, 'adds/databaseInfo.html')

def addTechMan(request):
    data = []

    cuss = CustomerInfo.objects.all()
    for c in cuss:
        tempDict = {}
        tempDict['cus'] = c

        tempDict['prodMan'] = ProductManagerHistory.objects.filter(customer=c)
        tempDict['techMan'] = TechnicalManagerHistory.objects.filter(
            customer=c)

        if len(tempDict['prodMan']) > 0:
            tempDict['prodMan'] = tempDict['prodMan'][len(
                tempDict['prodMan'])-1]

        if len(tempDict['techMan']) > 0:
            tempDict['techMan'] = tempDict['techMan'][len(
                tempDict['techMan'])-1]

        tempHist = ProductHistory.objects.filter(customer=c)
        tempDict['prodHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['prodHist']:
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['prodHist'][t.productversion.productmodule.pk].prodInstallationTime) > str(t.prodInstallationTime):
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

        tempHist = TestProductHistory.objects.filter(customer=c)
        tempDict['testProdHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['testProdHist']:
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['testProdHist'][t.productversion.productmodule.pk].testInstallationTime) > str(t.testInstallationTime):
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t
        
        data.append(tempDict)
        dataToSend = {
            'cus': CustomerInfo.objects.all(),
            'prodMan': ProductManagerHistory.objects.all(),
            'techMan': TechnicalManagerHistory.objects.all(),
            'db': DatabaseInfo.objects.all(),
            'dbHis': DatabaseVersion.objects.all(),
            'server': ServerInfo.objects.all(),
            'svHis': ServerVersion.objects.all(),
            'prod': ProductInfo.objects.all(),
            'prodMod': ProductModule.objects.all(),
            'prodVer': ProductVersion.objects.all(),
            'prodLoadTime': ProductHistory.objects.all(),
            'testLoadTime': TestProductHistory.objects.all(),
            'infHis': InfinaWorkerHistory.objects.all(),
            'data' : data
    }

    return render(request, 'adds/technicalManager.html', dataToSend)


def edit(request):

    if request.method == "POST":
        req=request.POST
        if req['edit_what'] == "editCustomer":
            pk1=req['pk']
            c = CustomerInfo.objects.get(pk=pk1)
            c.customerName = req['cus_name']
            c.save()
            return redirect('add')

        elif req['edit_what'] == "editProdMan":
            pk1=req['pk']
            p = ProductManagerHistory.objects.get(pk=pk1)
            p.prodManName = req['prodMan_name']
            p.prodManEmail = req['prodMan_email']
            p.prodManPhoneNumber = req['prodMan_phone']
            p.whenIsProdManResponsible = req['prodMan_date']
            p.save()
            return redirect('add')

        elif req['edit_what'] == "techMan":
            pk1=req['pk']
            t = TechnicalManagerHistory.objects.get(pk=pk1)
            t.techManName = req['techMan_name']
            t.techManEmail = req['techMan_email']
            t.prodManPhoneNumber = req['techMan_phone']
            t.whenIsTechManResponsible = req['techMan_date']
            t.save()
            return redirect('add')
        
        elif req['edit_what'] == "editProd":
            pk1=req['pk']
            p = ProductInfo.objects.get(pk=pk1)
            p.productName = req['prodName']
            p.save()
            return redirect('add')
        
        elif req['edit_what'] == "editProdMod":
            pk1=req['id']
            pm = ProductModule.objects.get(pk=pk1)
            pmp=req['pmp']
            pm.product=ProductInfo.objects.get(pk=pmp)
            pm.moduleName = req['prodModName']
            pm.save()
            return redirect('add')
        elif req['edit_what'] == "editProdVer":
            pk1=req['prodMod']
            pk2=req['id']
            p=ProductVersion.objects.get(pk=pk2)
            pm = ProductModule.objects.get(pk=pk1)
            p.productVersionName=req['prodVerName']
            p.save()
            return redirect('add')
        elif req['edit_what'] == "editDB":
            pk1=req['id']
            d=DatabaseInfo.objects.get(pk=pk1)
            d.databaseName=req['db_name']
            d.save()
            return redirect('add')
        elif req['edit_what'] == "editDbVer":
            pk1=req['id']
            d=DatabaseVersion.objects.get(pk=pk1)
            d.databaseVersionName=req['dbVer_name']
            d.save()
            return redirect('add')
        elif req['edit_what'] == "editServer":
            pk1=req['id']
            d=ServerInfo.objects.get(pk=pk1)
            d.serverName=req['server_name']
            d.save()
            return redirect('add')
        elif req['edit_what'] == "editServerVer":
            pk1=req['id']
            pk2=req['server']
            d=ServerVersion.objects.get(pk=pk1)
            d.server=ServerInfo.objects.get(pk=pk2)
            d.serverVersionName=req['svVer_name']

            d.save()
            return redirect('add')

    what = request.GET['what']
    if what == 'cus':
        pk1 = request.GET['id']
        cusData = CustomerInfo.objects.filter(pk=pk1)
        dataToSend = {
            'cus': cusData
        }
        return render(request, 'edits/customer.html', dataToSend)
    elif what == 'prodMan':
        pk1 = request.GET['id']
        prodData = ProductManagerHistory.objects.filter(pk=pk1)
        dataToSend = {
            'prodData': prodData
        }
        return render(request, 'edits/prodMan.html', dataToSend)
    elif what == 'techMan':
        pk1 = request.GET['id']
        techData = TechnicalManagerHistory.objects.filter(pk=pk1)
        dataToSend = {
            'techData': techData
        }
        return render(request, 'edits/techMan.html', dataToSend)
    elif what == 'prod':
        pk1 = request.GET['id']
        prodData = ProductInfo.objects.filter(pk=pk1)
        dataToSend = {
            'prodData': prodData
        }
        return render(request, 'edits/prod.html', dataToSend)
    elif what == 'prodMod':
        pk1 = request.GET['id']
        prodModData = ProductModule.objects.filter(pk=pk1)
        prodMods=ProductModule.objects.all()
        dataToSend = {
            'prodModData': prodModData,
            'prodMods' : prodMods
        }
        return render(request, 'edits/prodMod.html', dataToSend)
    elif what == 'prodVer':
        pk1 = request.GET['id']
        prodVerData = ProductVersion.objects.get(pk=pk1)
        prodVers=ProductVersion.objects.all()
        prodMods=ProductModule.objects.all()
        dataToSend = {
            'prodVerData': prodVerData,
            'prodVers' : prodVers,
            'prodMods' : prodMods
        }
        return render(request, 'edits/prodVer.html', dataToSend)
    elif what == 'db':
        pk1 = request.GET['id']
        dbData = DatabaseInfo.objects.get(pk=pk1)
        dataToSend = {
            'dbData': dbData
            }
        return render(request, 'edits/db.html', dataToSend)
    elif what == 'dbVer':
        pk1 = request.GET['id']
        dbVerData = DatabaseVersion.objects.get(pk=pk1)
        dbDatas=DatabaseInfo.objects.all()
        dataToSend = {
            'dbVerData': dbVerData,
            'dbDatas' : dbDatas
            }
        return render(request, 'edits/dbVer.html', dataToSend)
    elif what == 'server':
        pk1 = request.GET['id']
        server = ServerInfo.objects.get(pk=pk1)
        dataToSend = {
            'server': server
            }
        return render(request, 'edits/server.html', dataToSend)
    elif what == 'serverVer':
        pk1 = request.GET['id']
        serverVer = ServerVersion.objects.get(pk=pk1)
        server = ServerInfo.objects.all()
        dataToSend = {
            'server': server,
            'serverVer' : serverVer
            }
        return render(request, 'edits/serverVer.html', dataToSend)