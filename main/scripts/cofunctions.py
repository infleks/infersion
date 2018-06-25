import json
from main.models import *


def cusHistToJSON():
    cus=CustomerInfo.objects.all()
    cusArr = []
    for i,c in enumerate(cus):
        cusArr.append([])
        cusArr[i].append(c.customerName)
        cusArr[i].append(c.customerSituation)
        
    jsonstr = json.dumps({'cusArr': cusArr})
    return jsonstr

def cusIdsToJSON():
    cus=CustomerInfo.objects.all()
    cusIdArr = []
    for c in cus:
        cusIdArr.append(c.pk)

    jsonstr = json.dumps({'cusIdArr':cusIdArr})
    return jsonstr

def prodHistTestHistToJSON():
    pH=list(ProductHistory.objects.all())
    pArr = []
    for i,p in enumerate(pH):
        pArr.append([])
        pArr[i].append(p.customer.customerName)
        pArr[i].append(p.productversion.productmodule.product.productName + ", " + p.productversion.productmodule.moduleName + ", " + p.productversion.productVersionName )
        pArr[i].append(p.prodInstallationTime.strftime("%d-%m-%Y"))
        pArr[i].append(p.serverversion.server.serverName + ", " + p.serverversion.serverVersionName)
        pArr[i].append(p.databaseversion.database.databaseName + ", " + p.databaseversion.databaseVersionName)
        pArr[i].append(p.user.userEmail)
    
    tpH=TestProductHistory.objects.all()
    tpArr = []
    for i,p in enumerate(tpH):
        tpArr.append([])
        tpArr[i].append(p.customer.customerName)
        tpArr[i].append(p.productversion.productmodule.product.productName + ", " + p.productversion.productmodule.moduleName + ", " + p.productversion.productVersionName )
        tpArr[i].append(p.testInstallationTime.strftime("%d-%m-%Y"))
        tpArr[i].append(p.serverversion.server.serverName + ", " + p.serverversion.serverVersionName)
        tpArr[i].append(p.databaseversion.database.databaseName + ", " + p.databaseversion.databaseVersionName)
        tpArr[i].append(p.user.userEmail)

    jsonstr = json.dumps({'pArr':pArr, 'tpArr':tpArr})
    return jsonstr


def prodHistTestHistIdsToJSON():
    pH=list(ProductHistory.objects.all())
    pArr = []
    for p in pH:
        pArr.append(p.pk)

    tpH=TestProductHistory.objects.all()
    tpArr = []
    for p in tpH:
        tpArr.append(p.pk)

    jsonstr = json.dumps({'pIdArr':pArr, 'tpIdArr':tpArr})
    return jsonstr

def displayHistToJSON():
    pH=list(ProductHistory.objects.all())
    pArr = []
    for i,p in enumerate(pH):
        pArr.append([])
        pArr[i].append("Canlı")
        pArr[i].append(p.productversion.productmodule.product.productName + ", " + p.productversion.productmodule.moduleName + ", " + p.productversion.productVersionName )
        pArr[i].append(p.prodInstallationTime.strftime("%d-%m-%Y"))
        pArr[i].append(p.databaseversion.database.databaseName + ", " + p.databaseversion.databaseVersionName)
        pArr[i].append(p.serverversion.server.serverName + ", " + p.serverversion.serverVersionName)
        pArr[i].append(p.user.userEmail)
    
    tpH=TestProductHistory.objects.all()
    tpArr = []
    for i,p in enumerate(tpH):
        tpArr.append([])
        tpArr[i].append("Test")
        tpArr[i].append(p.productversion.productmodule.product.productName + ", " + p.productversion.productmodule.moduleName + ", " + p.productversion.productVersionName )
        tpArr[i].append(p.testInstallationTime.strftime("%d-%m-%Y"))
        tpArr[i].append(p.databaseversion.database.databaseName + ", " + p.databaseversion.databaseVersionName)
        tpArr[i].append(p.serverversion.server.serverName + ", " + p.serverversion.serverVersionName)
        tpArr[i].append(p.user.userEmail)

    jsonstr = json.dumps({'pArr':pArr, 'tpArr':tpArr})
    return jsonstr


def displayHistIdsToJSON():
    pH=list(ProductHistory.objects.all())
    pArr = []
    for p in pH:
        pArr.append(p.pk)

    tpH=TestProductHistory.objects.all()
    tpArr = []
    for p in tpH:
        tpArr.append(p.pk)

    jsonstr = json.dumps({'pIdArr':pArr, 'tpIdArr':tpArr})
    return jsonstr
