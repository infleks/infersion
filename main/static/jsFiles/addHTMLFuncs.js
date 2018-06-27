
function customerUyariFunc(){
    $(document).ready(function () {
      var urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('where')) {
        var where = urlParams.get('where');
        $("#customerInfo").removeClass('show');
        $('#' + where).addClass('show');
      }
      else {
        $("#customerInfo").addClass('show');
      }
      if (urlParams.get('uyari')) {
        if (urlParams.get('uyari') == 1) {
          alert("Bu isimde bir kayıt zaten mevcut.");
          if (urlParams.get('where')) {
            window.location.href = '/main/manage?where=' + urlParams.get('where');
          }
          else {
            window.location.href = '/main/manage?where=customerInfo';
          }
  
        }
      }
  
    });
  
}

function cusTableFunc(data, dataId, urlCus){
    $(document).ready(function () {

      try {
        JSON.parse('{{jsondata.2|safe}}')['cusArr'].length;
      }
      catch (err) {
        kapat('customerInfo');
      }

      


      $('#cusTable').DataTable({
        data: data['cusArr'],
        columns: [{
          title: "Müşteri Adı"
        },
        {
          title: "Müşteri Durumu"
        }
        ]
      });

      $('#cusTable').find("thead").find("tr").append(
        '<th></th><th style="cursor: pointer;"><a style="color: whitesmoke; text-decoration: none;" href= '+urlCus+' > <div><i style="cursor: pointer; font-size:20px;" class="fas fa-plus-circle"></i>  Ekle</div></a></th>');

      var chldrn = $('#cusTable').find("tbody").children();
      var i = 0;
      for (i = 0; i < chldrn.length; i++) {
        $(chldrn[i]).append(
          '<td style="cursor: pointer;"><a class="benima" href="/main/edit?what=cus&id='
          + dataId['cusIdArr'][i]
          + '"> <div><i class="fas fa-edit" style="color: #be5254; font-size:20px; cursor: pointer;"></i>Düzenle</div></a></td>'
          + '<td><a id="delete" class="benima" href="/main/delete?what=customerInfo&id='
          + dataId['cusIdArr'][i]
          + '" style=" cursor: pointer;"><i class="fas fa-trash-alt" style="color: #be5254; font-size:20px; cursor: pointer;"></i>Sil</a></td>');

      }

    });
}

function prodHisTableFunc(data, dataId, urlProd) {
    

    $('#prodTable').DataTable({
      data: data['pArr'],
      columns: [{
        title: "Müşteri"
      },
      {
        title: "Ürün"
      },
      {
        title: "Yükleme Tarihi"
      },
      {
        title: "Sunucu"
      },
      {
        title: "Veri Tabanı"
      },
      {
        title: "Eklemeyi Yapan"
      },
      {
        title: "Ürün URL"
      },
      {
        title: "Veritabanı URL"
      }
      ]
    });

    $('#prodTable').find("thead").find("tr").append('<th></th><th style="cursor: pointer;"><a style="color: whitesmoke; text-decoration: none;" href= '+urlProd+' > <div><i style="cursor: pointer; font-size:20px;" class="fas fa-plus-circle"></i>  Ekle</div></a></th>');

    var chldrn = $('#prodTable').find("tbody").children();
    var i = 0;
    for (i = 0; i < chldrn.length; i++) {
      $(chldrn[i]).append(' <td style="cursor: pointer;"><a class="benima" href="/main/edit?what=prodHis&id=' + dataId['pIdArr'][i] + '"> <div><i class="fas fa-edit" style="color: #be5254; font-size:20px; cursor: pointer;"></i>Düzenle</div></a></td>' + '<td><a class="benima" id="delete" href="/main/delete?what=prodHis&id=' + dataId['pIdArr'][i] + '" style=" cursor: pointer;"><i class="fas fa-trash-alt" style="color: #be5254; font-size:20px; cursor: pointer;"></i>Sil</a></td>');
    }
    $(document).ready(function () {
      var prodVar = 1;
      if (chldrn.length > 0) {
        $('#addprodHis').removeClass('show');
        prodVar = 1;
      }
      else {
        $('#addtestHis').addClass('show');
        prodVar = 0;
      }
    });
}

function testHisTableFunc(data, dataId, urlTest) {
    
    $(document).ready(function () {

      $('#testTable').DataTable({
        data: data['tpArr'],
        columns: [{
          title: "Müşteri"
        },
        {
          title: "Ürün"
        },
        {
          title: "Yükleme Tarihi"
        },
        {
          title: "Sunucu"
        },
        {
          title: "Veri Tabanı"
        },
        {
          title: "Eklemeyi Yapan"
        },
        {
          title: "Ürün URL"
        },
        {
          title: "Veirtabanı URL"
        }
        ]
      });

      $('#testTable').find("thead").find("tr").append('<th></th><th style="cursor: pointer;"><a style="color: whitesmoke; text-decoration: none;" href='+urlTest+'> <div><i style="cursor: pointer; font-size:20px;" class="fas fa-plus-circle"></i>  Ekle</div></a></th>');

      var chldrn = $('#testTable').find("tbody").children();
      var i = 0;
      for (i = 0; i < chldrn.length; i++) {
        $(chldrn[i]).append(' <td style="cursor: pointer;"><a class="benima" href="/main/edit?what=testHis&id=' + dataId['tpIdArr'][i] + '"> <div><i class="fas fa-edit" style="color: #be5254; font-size:20px; cursor: pointer;"></i>Düzenle</div></a></td>' + '<td><a class="benima" id="delete" href="/main/delete?what=testHis&id=' + dataId['tpIdArr'][i] + '" style=" cursor: pointer;"><i class="fas fa-trash-alt" style="color: #be5254; font-size:20px; cursor: pointer;"></i>Sil</a></td>');
      }
      var testVar = 1;
      if (chldrn.length > 0) {
        $('#addtestHis').removeClass('show');
        testVar = 1;
      }
      else {
        $('#addtestHis').addClass('show');
        testVar = 0;
      }
    });
}

