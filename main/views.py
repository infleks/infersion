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
