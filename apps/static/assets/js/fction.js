 i=0;

function load_predict_image(id,dat){
            
    var data = {"idclient" : id, "fonction" : dat};
    var url=base_url+"Admin/devenir";
    var result = post_ajax(url,data);
    //alert(result);
    var details = JSON.parse(result);
    //$('#plan').html(details);

        }

function load_predict_image(data){

            alert(data);
            
            var data = {"path" : data};
            var url=base_url+"Compte/requett";
            var result = post_ajax(url,data);
            //alert(result);
            var details = JSON.parse(result);
            //$('#plan').html(details);

        }



function validemande(data){

            //alert(data);          
            var data = {"idclient" : data};
            var url=base_url+"Admin/validemande";
            var result = post_ajax(url,data);
            //alert(result);
            location.reload();
            var details = JSON.parse(result);
            //reload();
            //$('#plan').html(details);
        }

function annuldemande(data){

            //alert(data);          
            var data = {"idclient" : data};
            var url=base_url+"Admin/annuldemande";
            var result = post_ajax(url,data);
            //alert(result);
            location.reload();
            var details = JSON.parse(result);
            //reload();
            //$('#plan').html(details);
        }



function lespays(){
    //alert(document.getElementById('countryCode').value(2));
    //alert($('#countryCode').val());

}



 function post_ajax(url, data) {
    var result = '';
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function(response) {
            result = response;
            //location.reload();
        },
        error: function(response) {
            result = 'error';
        },
        async: false
        });
        
        return result;
}

 function get_ajax(url, data) {
    var result = '';
    $.ajax({
        type: "GET",
        url: url,
        data: data,
        success: function(response) {
            result = response;
            //location.reload();
        },
        error: function(response) {
            result = 'error';
        },
        async: false
        });
        
        return result;
}