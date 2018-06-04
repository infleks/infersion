from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# Create your views here.

def display(request):
    cI = CustomerInfo.objects.all()
    data = []
    for c in cI:
        data.append({
            'cus_name': c.customerName
        })

    return render(request, 'index.html', {'data':data})

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
            '''
        elif p['add_what'] == 'prodVer':
            v = ProductVersion()
            v.module = ProductModule.objects.get(pk=p['module_id'])
            v.versionName = p['prodVer_name']
            v.prodVersionUpdateTime = ['prodVer_date']
            v.save()
        elif p['add_what'] == 'tprodVer':
            tV = TestProductVersion()
            tV.module = ProductModule.objects.get(pk=p['module_id'])
            tV.testProductVersionName = p['tprodVer_name']
            tV.testProductVersionUpdateTime = p['tprodVer_date']
            tV.save()
            '''                    
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
            iH.testhistory = TestProductHistory.objects.get(pk=p['tprodHis_id'])
            iH.workerName = p['infHis_name']
            iH.workerSurname = p['infHis_surname']
            iH.savingTime = p['infHis_date']
            iH.save()

    dataToSend = {
        'cus' : CustomerInfo.objects.all(),
        'prodMan': ProductManagerHistory.objects.all(),
        'techMan' : TechnicalManagerHistory.objects.all(),
        'db'  : DatabaseInfo.objects.all(),
        'dbHis'  : DatabaseVersion.objects.all(),
        'server' : ServerInfo.objects.all(),
        'svHis' : ServerVersion.objects.all(),
        'prod' : ProductInfo.objects.all(),
        'prodMod' : ProductModule.objects.all(),
        'prodVer' : ProductVersion.objects.all(),
        'prodLoadTime' : ProductHistory.objects.all(),
        'testLoadTime' : TestProductHistory.objects.all(),
        'infHis' : InfinaWorkerHistory.objects.all(),
    }

    return render(request, 'add.html', dataToSend)