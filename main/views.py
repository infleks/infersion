from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import datetime
from main.scripts.cofunctions import *
from django.contrib import messages
# Create your views here.


def login_view(request):
    if request.method == "POST":
        p = request.POST
        userr = UserInfo.objects.filter(
            userEmail=p['user_email'], userPassword=p['user_password'])
    
        if(len(userr) > 0):
            user = userr[0]
            request.session['user_id'] = user.pk
            request.session['user_email'] = user.userEmail
            return redirect('display')
        else:
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {})
def logout_view(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return render(request, 'registration/logout.html', {})

def display(request):   
    if 'user_id' not in request.session.keys():
        return redirect('login')
    data = []

    cuss = CustomerInfo.objects.all()

    for c in cuss:
        tempDict = {}
        tempDict['cus'] = c

        tempDict['prodMan'] = [p for p in ProductManagerHistory.objects.filter(customer=c).order_by('pk')]
        tempDict['techMan'] = [t for t in TechnicalManagerHistory.objects.filter(customer=c).order_by('pk')]

        tempDict['prodMan'] = tempDict['prodMan'][-1] if len(tempDict['prodMan'])>0 else tempDict['prodMan']
        tempDict['techMan'] = tempDict['techMan'][-1] if len(tempDict['techMan'])>0 else tempDict['techMan']

        tempHist = ProductHistory.objects.filter(customer=c)
        tempDict['prodHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['prodHist']:
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['prodHist'][t.productversion.productmodule.pk].prodInstallationTime) < str(t.prodInstallationTime):
                tempDict['prodHist'][t.productversion.productmodule.pk] = t

        tempHist = TestProductHistory.objects.filter(customer=c)
        tempDict['testProdHist'] = {}
        for t in tempHist:
            if t.productversion.productmodule.pk not in tempDict['testProdHist']:
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t

            if str(tempDict['testProdHist'][t.productversion.productmodule.pk].testInstallationTime) < str(t.testInstallationTime):
                tempDict['testProdHist'][t.productversion.productmodule.pk] = t

        data.append(tempDict)

    return render(request, 'display.html', {'data': data})


def manage(request):
    dataToSend = {}
    if 'user_id' not in request.session.keys():
        return redirect('login')
    users = UserInfo.objects.get(pk=request.session['user_id'])
    if users.userPermission == "2":
        return redirect('/main?uyari=2') 
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
            'users' :UserInfo.objects.get(pk=request.session['user_id']),
            'data' : data,
            'jsondata' : [prodHistTestHistToJSON(), prodHistTestHistIdsToJSON(), cusHistToJSON(), cusIdsToJSON()]

    }

    return render(request, 'add.html', dataToSend)

def add(request):
    if 'user_id' not in request.session.keys():
        return redirect('login')
    users = UserInfo.objects.get(pk=request.session['user_id'])
    if users.userPermission == "2":
        return redirect('display')
    if(request.method == 'POST'):
        p = request.POST
        if p['add_what'] == "cus":
            varMi=1
            try: 
                CustomerInfo.objects.get(customerName__iexact=p['cus_name'])
            except CustomerInfo.DoesNotExist:
                varMi=0
            if varMi==0:
                c = CustomerInfo()
                c.customerName = p['cus_name']
                c.customerSituation = p['cus_situ']
                c.save()
                return redirect("/main/manage?where=customerInfo")
            else:          
                return redirect("/main/manage?where=customerInfo&uyari=1")
            
        elif p['add_what'] == "prodMan":
            varMi=1
            try:
                ProductManagerHistory.objects.get(customer=CustomerInfo.objects.get(pk=p['cus_id']), prodManName__iexact=p['prodMan_name'], prodManEmail__iexact=p['prodMan_email'], prodManPhoneNumber=p['prodMan_phone'])
            except ProductManagerHistory.DoesNotExist:
                varMi=0
            if varMi==0:
                pM = ProductManagerHistory()
                pM.customer = CustomerInfo.objects.get(pk=p['cus_id'])
                pM.prodManName = p['prodMan_name']
                pM.prodManEmail = p['prodMan_email']
                pM.prodManPhoneNumber = p['prodMan_phone']
                pM.whenIsProdManResponsible = p['prodMan_date']
                pM.save()
                return redirect("/main/manage?where=prodMans")
            else:
                return redirect("/main/manage?where=prodMans&uyari=1")
        elif p['add_what'] == "techMan":
            varMi=1
            try:
                TechnicalManagerHistory.objects.get(customer=CustomerInfo.objects.get(pk=p['cus_id']), techManName__iexact=p['techMan_name'], techManEmail__iexact=p['techMan_email'], techManPhoneNumber=p['techMan_phone'])
            except TechnicalManagerHistory.DoesNotExist:
                varMi=0
            if varMi==0:

                tM = TechnicalManagerHistory()
                tM.customer = CustomerInfo.objects.get(pk=p['cus_id'])
                tM.techManName = p['techMan_name']
                tM.techManEmail = p['techMan_email']
                tM.techManPhoneNumber = p['techMan_phone']
                tM.whenIsTechManResponsible = p['techMan_date']
                tM.save()
                return redirect("/main/manage?where=techMans")
            else:
                return redirect("/main/manage?where=techMans&uyari=1")
        elif p['add_what'] == "db":
            varMi=1
            try:
                DatabaseInfo.objects.get(databaseName__iexact=p['db_name'])
            except DatabaseInfo.DoesNotExist:
                varMi=0
            if varMi==0:
                d = DatabaseInfo()
                d.databaseName = p['db_name']
                d.save()
                return redirect("/main/manage?where=databases")
            else:
                return redirect("/main/manage?where=databases&uyari=1")
            
        elif p['add_what'] == "dbHis":
            varMi=1
            try:
                DatabaseVersion.objects.get(databaseVersionName__iexact=p['dbVer_name'], database=DatabaseInfo.objects.get(pk=p['db_id']) )
            except DatabaseVersion.DoesNotExist:
                varMi=0
            if varMi==0:
                dH = DatabaseVersion()
                dH.database = DatabaseInfo.objects.get(pk=p['db_id'])
                dH.databaseVersionName = p['dbVer_name']
                dH.save()
                return redirect("/main/manage?where=dbVers")
            else:
                return redirect("/main/manage?where=dbVers&uyari=1")

        elif p['add_what'] == "server":
            varMi=1
            try:
                ServerInfo.objects.get(serverName__iexact=p['server_name'])
            except ServerInfo.DoesNotExist:
                varMi=0
            if varMi==0:
                s = ServerInfo()
                s.serverName = p['server_name']
                s.save()
                return redirect("/main/manage?where=servers")
            else:
                return redirect("/main/manage?where=servers&uyari=1")
        elif p['add_what'] == "svHis":
            varMi=1
            try:
                ServerVersion.objects.get(serverVersionName__iexact=p['svVer_name'], server=ServerInfo.objects.get(pk=p['sv_id']) )
            except ServerVersion.DoesNotExist:
                varMi=0
            if varMi==0:
                sH = ServerVersion()
                sH.server = ServerInfo.objects.get(pk=p['sv_id'])
                sH.serverVersionName = p['svVer_name']
                sH.save()
                return redirect("/main/manage?where=serverVer")
            else:
                return redirect("/main/manage?where=serverVer&uyari=1")
        elif p['add_what'] == 'prod':
            varMi=1
            try:
                ProductInfo.objects.get(productName__iexact=p['prod_name'])
            except ProductInfo.DoesNotExist:
                varMi=0
            if varMi==0:
                pr = ProductInfo()
                pr.productName = p['prod_name']
                pr.save()
                return redirect("/main/manage?where=products")
            else:
                return redirect("/main/manage?where=products&uyari=1")
        elif p['add_what'] == 'prodMod':
            varMi=1
            try:
                ProductModule.objects.get(moduleName__iexact=p['prodMod_name'], product=ProductInfo.objects.get(pk=p['prod_id']) )
            except ProductModule.DoesNotExist:
                varMi=0
            if varMi==0:
                prM = ProductModule()
                prM.product = ProductInfo.objects.get(pk=p['prod_id'])
                prM.moduleName = p['prodMod_name']
                prM.save()
                return redirect("/main/manage?where=prodModule")
            else:
                return redirect("/main/manage?where=prodModule&uyari=1")
        elif p['add_what'] == 'prodVer':
            varMi=1
            try:
                ProductVersion.objects.get(productVersionName__iexact=p['prodVer_name'], productmodule=ProductModule.objects.get(pk=p['prodMod_id']) )
            except ProductVersion.DoesNotExist:
                varMi=0
            if varMi==0:
                pV = ProductVersion()
                pV.productmodule = ProductModule.objects.get(pk=p['prodMod_id'])
                pV.productVersionName = p['prodVer_name']
                pV.save()
                return redirect("/main/manage?where=prodVer")
            else:
                return redirect("/main/manage?where=prodVer&uyari=1")
        elif p['add_what'] == 'prodLoadTime':
            varMi=1
            try:
                ProductHistory.objects.get(customer=CustomerInfo.objects.get(pk=p['cus_id']), productversion=ProductVersion.objects.get(pk=p['prodVers_id']), databaseversion=DatabaseVersion.objects.get(pk=p['dbVer_id']), serverversion=ServerVersion.objects.get(pk=p['svVer_id']) )
            except ProductHistory.DoesNotExist:
                varMi=0
            if varMi==0:
                pH = ProductHistory()
                pH.customer = CustomerInfo.objects.get(pk=p['cus_id'])
                pH.productversion = ProductVersion.objects.get(pk=p['prodVers_id'])
                pH.databaseversion = DatabaseVersion.objects.get(pk=p['dbVer_id'])
                pH.serverversion = ServerVersion.objects.get(pk=p['svVer_id'])
                pH.user = UserInfo.objects.get(pk=request.session['user_id'])
                pH.prodInstallationTime = p['prodLoadTime_date']
                pH.url = p['url_name']
                pH.save()
                return redirect("/main/manage?where=prodHis")
            else:
                return redirect("/main/manage?where=prodHis&uyari=1")
        elif p['add_what'] == 'testLoadTime':
            varMi=1
            try:
                TestProductHistory.objects.get(customer=CustomerInfo.objects.get(pk=p['cus_id']), productversion=ProductVersion.objects.get(pk=p['prodVers_id']), databaseversion=DatabaseVersion.objects.get(pk=p['dbVer_id']), serverversion=ServerVersion.objects.get(pk=p['svVer_id']) )
            except TestProductHistory.DoesNotExist:
                varMi=0
            if varMi==0:
                tH = TestProductHistory()
                tH.customer = CustomerInfo.objects.get(pk=p['cus_id'])
                tH.productversion = ProductVersion.objects.get(pk=p['prodVers_id'])
                tH.databaseversion = DatabaseVersion.objects.get(pk=p['dbVer_id'])
                tH.serverversion = ServerVersion.objects.get(pk=p['svVer_id'])
                tH.user = UserInfo.objects.get(pk=request.session['user_id'])
                tH.testInstallationTime = p['testLoadTime_date']
                tH.url = p['url_name']
                tH.save()
                return redirect("/main/manage?where=testHis")
            else:
                return redirect("/main/manage?where=testHis&uyari=1")
          
    return redirect('manage')

def detail(request):

    if request.method != "GET":
        return redirect('display')

    if 'id' not in request.GET.keys():
        return redirect('display')

    pk1 = request.GET['id']
    cusData = CustomerInfo.objects.get(pk=pk1)
    prodData = ProductHistory.objects.filter(customer=cusData)
    testData = TestProductHistory.objects.filter(customer=cusData)


    dataToSend = {
        'prodData': prodData,
        'testData': testData,
        'jsondata' : [displayHistToJSON(prodData, testData), displayHistIdsToJSON(prodData, testData)]
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
            'data' : data
    }

    return render(request, 'adds/productManager.html', dataToSend)



def addCus(request):
    return render(request, 'adds/customerInfo.html')


def addProd(request):
    return render(request, 'adds/productInfo.html')

def addProdMod(request):
    prods=ProductInfo.objects.all()
    dataToSend={
        'prods' : prods
    }
    return render(request, 'adds/productModule.html', dataToSend)

def addServer(request):
    return render(request, 'adds/serverInfo.html')

def addProdHis(request):
    cus=CustomerInfo.objects.all()
    prodVer= ProductVersion.objects.all()
    dbHis= DatabaseVersion.objects.all()
    svHis=ServerVersion.objects.all()

    dataToSend={
        'cus':cus,
        'prodVer':prodVer,
        'dbHis': dbHis,
        'svHis':svHis


    }

    return render(request, 'adds/productHistory.html', dataToSend)
def addTestHis(request):
    cus=CustomerInfo.objects.all()
    prodVer= ProductVersion.objects.all()
    dbHis= DatabaseVersion.objects.all()
    svHis=ServerVersion.objects.all()

    dataToSend={
        'cus':cus,
        'prodVer':prodVer,
        'dbHis': dbHis,
        'svHis':svHis


    }
    return render(request, 'adds/testProductHistory.html', dataToSend)

def addProdVer(request):
    prodMod=ProductModule.objects.all()
    dataToSend={
        'prodMod' : prodMod
    }
    return render(request, 'adds/productVersion.html', dataToSend)

def addDbVer(request):
    db=DatabaseInfo.objects.all()
    dataToSend={
        'db' : db,
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
            'data' : data
    }

    return render(request, 'adds/technicalManager.html', dataToSend)


def edit(request):
    if 'user_id' not in request.session.keys():
        return redirect('login')
    if request.method == "POST":
        req=request.POST
        if req['edit_what'] == "editCustomer":
            varMi=1
            try:
                CustomerInfo.objects.get(customerName=req['cus_name'], customerSituation=req['cus_situ'])
            except CustomerInfo.DoesNotExist:
                varMi=0
            if varMi==0:
                pk1=req['pk']
                c = CustomerInfo.objects.get(pk=pk1)
                c.customerName = req['cus_name']
                c.customerSituation = req['cus_situ']
                c.save()
                return redirect("/main/manage?where=customerInfo")
            else:          
                return redirect("/main/manage?where=customerInfo&uyari=1")

        elif req['edit_what'] == "editProdMan":
            varMi=1
            try:
                ProductManagerHistory.objects.get(customer=CustomerInfo.objects.get(pk=req['cus_id']), prodManName=req['prodMan_name'], prodManEmail=req['prodMan_email'], prodManPhoneNumber=req['prodMan_phone'], whenIsProdManResponsible = req['prodMan_date'])
            except ProductManagerHistory.DoesNotExist:
                varMi=0
            if varMi==0:

                pk1=req['pk']
                p = ProductManagerHistory.objects.get(pk=pk1)
                p.prodManName = req['prodMan_name']
                p.prodManEmail = req['prodMan_email']
                p.prodManPhoneNumber = req['prodMan_phone']
                p.customer=CustomerInfo.objects.get(pk=req['cus_id'])
                p.whenIsProdManResponsible = req['prodMan_date']
                p.save()
                return redirect("/main/manage?where=prodMans")
            else:
                return redirect("/main/manage?where=prodMans&uyari=1")

        elif req['edit_what'] == "editTechMan":
            varMi=1
            try:
                TechnicalManagerHistory.objects.get(customer=CustomerInfo.objects.get(pk=req['cus_id']), techManName=req['techMan_name'], techManEmail=req['techMan_email'], techManPhoneNumber=req['techMan_phone'], whenIsTechManResponsible = req['techMan_date'])
            except TechnicalManagerHistory.DoesNotExist:
                varMi=0
            if varMi==0:

                pk1=req['id']
                t = TechnicalManagerHistory.objects.get(pk=pk1)
                t.techManName = req['techMan_name']
                t.techManEmail = req['techMan_email']
                t.techManPhoneNumber = req['techMan_phone']
                t.whenIsTechManResponsible = req['techMan_date']
                t.save()
                return redirect("/main/manage?where=techMans")
            else:
                return redirect("/main/manage?where=techMans&uyari=1")
        
        elif req['edit_what'] == "editProd":
            varMi=1
            try:
                ProductInfo.objects.get(productName=req['prodName'])
            except ProductInfo.DoesNotExist:
                varMi=0
            if varMi==0:
                pk1=req['pk']
                p = ProductInfo.objects.get(pk=pk1)
                p.productName = req['prodName']
                p.save()
                return redirect("/main/manage?where=products")
            else:
                return redirect("/main/manage?where=products&uyari=1")

        
        elif req['edit_what'] == "editProdMod":
            varMi=1
            try:
                ProductModule.objects.get(moduleName=req['prodModName'], product=ProductInfo.objects.get(pk=req['pmp']) )
            except ProductModule.DoesNotExist:
                varMi=0
            if varMi==0:
                pk1=req['id']
                pm = ProductModule.objects.get(pk=pk1)
                pmp=req['pmp']
                pm.product=ProductInfo.objects.get(pk=pmp)
                pm.moduleName = req['prodModName']
                pm.save()
                return redirect("/main/manage?where=prodModule")
            else:
                return redirect("/main/manage?where=prodModule&uyari=1")
        elif req['edit_what'] == "editProdVer":
            varMi=1
            try:
                ProductVersion.objects.get(productVersionName=req['prodVerName'], productmodule=ProductModule.objects.get(pk=req['prodMod']) )
            except ProductVersion.DoesNotExist:
                varMi=0
            if varMi==0:
                pk1=req['prodMod']
                pk2=req['id']
                p=ProductVersion.objects.get(pk=pk2)
                pm = ProductModule.objects.get(pk=pk1)
                p.productVersionName=req['prodVerName']
                p.save()
                return redirect("/main/manage?where=prodVer")
            else:
                return redirect("/main/manage?where=prodVer&uyari=1")
        elif req['edit_what'] == "editDB":
            varMi=1
            try:
                DatabaseInfo.objects.get(databaseName=req['db_name'])
            except DatabaseInfo.DoesNotExist:
                varMi=0
            if varMi==0:

                pk1=req['id']
                d=DatabaseInfo.objects.get(pk=pk1)
                d.databaseName=req['db_name']
                d.save()
                return redirect("/main/manage?where=databases")
            else:
                return redirect("/main/manage?where=databases&uyari=1")
        elif req['edit_what'] == "editDbVer":
            varMi=1
            try:
                DatabaseVersion.objects.get(databaseVersionName=req['dbVer_name'], database=DatabaseInfo.objects.get(pk=req['db_id']) )
            except DatabaseVersion.DoesNotExist:
                varMi=0
            if varMi==0:

                pk1=req['id']
                d=DatabaseVersion.objects.get(pk=pk1)
                d.databaseVersionName=req['dbVer_name']
                d.database=DatabaseInfo.objects.get(pk=req['db_id'])
                d.save()
                return redirect("/main/manage?where=dbVers")
            else:
                return redirect("/main/manage?where=dbVers&uyari=1")
        elif req['edit_what'] == "editServer":
            varMi=1
            try:
                ServerInfo.objects.get(serverName=req['server_name'])
            except ServerInfo.DoesNotExist:
                varMi=0
            if varMi==0:

                pk1=req['id']
                d=ServerInfo.objects.get(pk=pk1)
                d.serverName=req['server_name']
                d.save()
                return redirect("/main/manage?where=servers")
            else:
                return redirect("/main/manage?where=servers&uyari=1")
        elif req['edit_what'] == "editServerVer":
            varMi=1
            try:
                ServerVersion.objects.get(serverVersionName=req['svVer_name'], server=ServerInfo.objects.get(pk=req['server']) )
            except ServerVersion.DoesNotExist:
                varMi=0
            if varMi==0:
                pk1=req['id']
                pk2=req['server']
                d=ServerVersion.objects.get(pk=pk1)
                d.server=ServerInfo.objects.get(pk=pk2)
                d.serverVersionName=req['svVer_name']

                d.save()
                return redirect("/main/manage?where=serverVer")
            else:
                return redirect("/main/manage?where=serverVer&uyari=1")
        elif req['edit_what'] == "editProdHis":
            varMi=1
            try:
                ProductHistory.objects.get(customer=CustomerInfo.objects.get(pk=req['cus_id']), productversion=ProductVersion.objects.get(pk=req['prodVers_id']), databaseversion=DatabaseVersion.objects.get(pk=req['db']), serverversion=ServerVersion.objects.get(pk=req['server']), prodInstallationTime = req['prodLoadTime_date'] )
            except ProductHistory.DoesNotExist:
                varMi=0
            if varMi==0:

                pk1=req['id']
                pk2=req['server']
                pk3=req['db']
                pk4=req['cus_id']
                d=ProductHistory.objects.get(pk=pk1)
                d.customer=CustomerInfo.objects.get(pk=pk4)
                prodVer=req['prodVers_id']
                prodversion=ProductVersion.objects.get(pk=prodVer)
                prod=prodversion.productmodule.product
                s=ServerVersion.objects.get(pk=pk2)
                db=DatabaseVersion.objects.get(pk=pk3)
                d.serverversion=s
                d.databaseversion=db
                d.prodInstallationTime=req['prodLoadTime_date']
                d.productversion=prodversion
                d.url = req['url_name']

                d.save()
                return redirect("/main/manage?where=prodHis")
            else:
                return redirect("/main/manage?where=prodHis&uyari=1")
        elif req['edit_what'] == "editTestHis":
            varMi=1
            try:
                TestProductHistory.objects.get(customer=CustomerInfo.objects.get(pk=p['cus_id']), productversion=ProductVersion.objects.get(pk=p['prodVers_id']), databaseversion=DatabaseVersion.objects.get(pk=p['db']), serverversion=ServerVersion.objects.get(pk=p['server']), testInstallationTime = req['testLoadTime_date'] )
            except TestProductHistory.DoesNotExist:
                varMi=0
            if varMi==0:

                pk1=req['id']
                pk2=req['server']
                pk3=req['db']
                pk4=req['cus_id']
                d=TestProductHistory.objects.get(pk=pk1)
                d.customer=CustomerInfo.objects.get(pk=pk4)
                prodVer=req['prodVers_id']
                prodversion=ProductVersion.objects.get(pk=prodVer)
                prod=prodversion.productmodule.product
                s=ServerVersion.objects.get(pk=pk2)
                db=DatabaseVersion.objects.get(pk=pk3)
                d.serverversion=s
                d.databaseversion=db
                d.testInstallationTime=req['testLoadTime_date']
                d.productversion=prodversion
                d.url = req['url_name']

                d.save()
                return redirect("/main/manage?where=testHis")
            else:
                return redirect("/main/manage?where=testHis&uyari=1")

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
        prodData = ProductManagerHistory.objects.get(pk=pk1)
        tarih = datetime.strftime(prodData.whenIsProdManResponsible, "%Y-%m-%d")        
        cus=CustomerInfo.objects.all()
        dataToSend = {
            'prodData': prodData,
            'cus' : cus,
            'tarih': tarih
        }
        return render(request, 'edits/prodMan.html', dataToSend)
    elif what == 'techMan':
        pk1 = request.GET['id']
        techData = TechnicalManagerHistory.objects.get(pk=pk1)
        tarih = datetime.strftime(techData.whenIsTechManResponsible, "%Y-%m-%d")  
        cus=CustomerInfo.objects.all()
        dataToSend = {
            'techData': techData,
            'tarih' : tarih,
            'cus': cus
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
        prodModData = ProductModule.objects.get(pk=pk1)
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
    elif what == 'prodHis':
        pk1 = request.GET['id']
        prodHis = ProductHistory.objects.get(pk=pk1)
        cusId = prodHis.customer.pk
        prodHisDate = datetime.strftime(ProductHistory.objects.get(pk=pk1).prodInstallationTime, "%Y-%m-%d")
        svHis = ServerVersion.objects.all()
        dbHis= DatabaseVersion.objects.all()
        c=CustomerInfo.objects.get(pk=cusId)
        cus=CustomerInfo.objects.all()
        prodMan = ProductManagerHistory.objects.filter(customer=c)
        techMan = TechnicalManagerHistory.objects.filter(customer=c)
        prodVer= ProductVersion.objects.all()

        
        dataToSend = {
            'svHis': svHis,
            'prodMan' : prodMan,
            'techMan' : techMan,
            'dbHis' : dbHis,
            'cus' : cus,
            'prodVer' : prodVer,
            'prodHis' : prodHis,
            'prodHisDate' : prodHisDate
            }
        return render(request, 'edits/prodHis.html', dataToSend)
    elif what == 'testHis':
        pk1 = request.GET['id']
        testHis = TestProductHistory.objects.get(pk=pk1)
        cusId = testHis.customer.pk
        testHisDate = datetime.strftime(TestProductHistory.objects.get(pk=pk1).testInstallationTime, "%Y-%m-%d")
        svHis = ServerVersion.objects.all()
        dbHis= DatabaseVersion.objects.all()
        c=CustomerInfo.objects.get(pk=cusId)
        cus=CustomerInfo.objects.all()
        prodMan = ProductManagerHistory.objects.filter(customer=c)
        techMan = TechnicalManagerHistory.objects.filter(customer=c)
        prodVer= ProductVersion.objects.all()

        
        dataToSend = {
            'svHis': svHis,
            'prodMan' : prodMan,
            'techMan' : techMan,
            'dbHis' : dbHis,
            'cus' : cus,
            'prodVer' : prodVer,
            'testHis' : testHis,
            'testHisDate' : testHisDate
            }
       
        return render(request, 'edits/testHis.html', dataToSend)

def delete(request):
    if request.method == "GET":
        req=request.GET
        what=req['what']
        pk1=req['id']
        if what=="customerInfo":
            d=CustomerInfo.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=customerInfo")

           
        elif what=="db":
            d=DatabaseInfo.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=databases")

            
        elif what=="dbVer":
            d=DatabaseVersion.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=dbVers")

        elif what=="prodHis":
            d=ProductHistory.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=prodHis")

        elif what=="prod":
            d=ProductInfo.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=products")
        elif what=="prodMan":
            d=ProductManagerHistory.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=prodMans")
        elif what=="prodMod":
            d=ProductModule.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=prodModule")
        elif what=="prodVer":
            d=ProductVersion.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=prodVer")
        elif what=="sv":
            d=ServerInfo.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=servers")
        elif what=="svVer":
            d=ServerVersion.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=serverVer")
        elif what=="techMan":
            d=TechnicalManagerHistory.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=techMans")
        elif what=="testHis":
            d=TestProductHistory.objects.get(pk=pk1)
            d.delete()
            return redirect("/main/manage?where=testHis")