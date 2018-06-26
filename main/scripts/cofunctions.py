import json
from main.models import *
from django.db.models.functions import Lower

def cusHistToJSON():
    cus=CustomerInfo.objects.all().order_by(Lower('customerName'))
    cusArr = []
    for i,c in enumerate(cus):
        cusArr.append([])
        cusArr[i].append(c.customerName)
        cusArr[i].append(c.customerSituation)
        
    jsonstr = json.dumps({'cusArr': cusArr})
    return jsonstr

def cusIdsToJSON():
    cus=CustomerInfo.objects.all().order_by(Lower('customerName'))
    cusIdArr = []
    for c in cus:
        cusIdArr.append(c.pk)

    jsonstr = json.dumps({'cusIdArr':cusIdArr})
    return jsonstr

def prodHistTestHistToJSON():
    pH=list(ProductHistory.objects.all())
    pArr = []
    for i,p in enumerate(pH):
        if p.customer.customerSituation == "Aktif":
            pArr.append([])
            pArr[-1].append(p.customer.customerName)
            pArr[-1].append(p.productversion.productmodule.product.productName + ", " + p.productversion.productmodule.moduleName + ", " + p.productversion.productVersionName )
            pArr[-1].append(p.prodInstallationTime.strftime("%d-%m-%Y"))
            pArr[-1].append(p.serverversion.server.serverName + ", " + p.serverversion.serverVersionName)
            pArr[-1].append(p.databaseversion.database.databaseName + ", " + p.databaseversion.databaseVersionName)
            pArr[-1].append(p.user.userEmail)
    
    tpH=TestProductHistory.objects.all()
    tpArr = []
    for i,p in enumerate(tpH):
        if p.customer.customerSituation == "Aktif":
            tpArr.append([])
            tpArr[-1].append(p.customer.customerName)
            tpArr[-1].append(p.productversion.productmodule.product.productName + ", " + p.productversion.productmodule.moduleName + ", " + p.productversion.productVersionName )
            tpArr[-1].append(p.testInstallationTime.strftime("%d-%m-%Y"))
            tpArr[-1].append(p.serverversion.server.serverName + ", " + p.serverversion.serverVersionName)
            tpArr[-1].append(p.databaseversion.database.databaseName + ", " + p.databaseversion.databaseVersionName)
            tpArr[-1].append(p.user.userEmail)

    jsonstr = json.dumps({'pArr':pArr, 'tpArr':tpArr})
    return jsonstr


def prodHistTestHistIdsToJSON():
    pH=list(ProductHistory.objects.all())
    pArr = []
    for p in pH:
        if p.customer.customerSituation == "Aktif":
            pArr.append(p.pk)

    tpH=TestProductHistory.objects.all()
    tpArr = []
    for p in tpH:
        if p.customer.customerSituation == "Aktif":
            tpArr.append(p.pk)

    jsonstr = json.dumps({'pIdArr':pArr, 'tpIdArr':tpArr})
    return jsonstr

def displayHistToJSON():
    pH=list(ProductHistory.objects.all())
    pArr = []
    for i,p in enumerate(pH):
        if p.customer.customerSituation == "Aktif":
            pArr.append([])
            pArr[-1].append("Canlı")
            pArr[-1].append(p.productversion.productmodule.product.productName + ", " + p.productversion.productmodule.moduleName + ", " + p.productversion.productVersionName )
            pArr[-1].append(p.prodInstallationTime.strftime("%d-%m-%Y"))
            pArr[-1].append(p.databaseversion.database.databaseName + ", " + p.databaseversion.databaseVersionName)
            pArr[-1].append(p.serverversion.server.serverName + ", " + p.serverversion.serverVersionName)
            pArr[-1].append(p.user.userEmail)
    
    tpH=TestProductHistory.objects.all()
    tpArr = []
    for i,p in enumerate(tpH):
        if p.customer.customerSituation == "Aktif":
            tpArr.append([])
            tpArr[-1].append("Test")
            tpArr[-1].append(p.productversion.productmodule.product.productName + ", " + p.productversion.productmodule.moduleName + ", " + p.productversion.productVersionName )
            tpArr[-1].append(p.testInstallationTime.strftime("%d-%m-%Y"))
            tpArr[-1].append(p.databaseversion.database.databaseName + ", " + p.databaseversion.databaseVersionName)
            tpArr[-1].append(p.serverversion.server.serverName + ", " + p.serverversion.serverVersionName)
            tpArr[-1].append(p.user.userEmail)

    jsonstr = json.dumps({'pArr':pArr, 'tpArr':tpArr})
    return jsonstr


def displayHistIdsToJSON():
    pH=list(ProductHistory.objects.all())
    pArr = []
    for p in pH:
        if p.customer.customerSituation == "Aktif":
            pArr.append(p.pk)

    tpH=TestProductHistory.objects.all()
    tpArr = []
    for p in tpH:
        if p.customer.customerSituation == "Aktif":
            tpArr.append(p.pk)

    jsonstr = json.dumps({'pIdArr':pArr, 'tpIdArr':tpArr})
    return jsonstr
