$(document).ready(function(){
    
    /*  This is for transfering CSRF with $.ajax calls */
    /****************************************************/
    function getCookie(cname){
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++){
	    var c = ca[i].trim();
	    if (c.indexOf(name)==0) return c.substring(name.length,c.length);
	  }
	return "";
    }
    

    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    /*  This is for transfering CSRF with $.ajax calls */
    /****************************************************/
    
    
    jQuery.validator.addMethod("endGreaterStart", function(endTime, element) {
        var startTime = $("#createSession-form input[name='startTime']").val();
        
        if (startTime >= endTime) {
            return false;
        }else{
         return true; 
        }
      }, "must be after start time");
    
    $('form').each(function(){
        $(this).validate();
    });
    
    
    
    
    $("#createSession-form").ajaxForm({ 
            success:       function(responseText){
                console.log(responseText);
                if (responseText.error) {
                    alert(responseText.error);
                }else{
                    window.location.href = "/classView/"+responseText.groupID+"/";
                }
            },
            dataType:  'json',
            timeout:   4000 
        });
    
    
    
    
    $("#editSession-form").ajaxForm({ 
            success:       function(responseText){
                console.log(responseText);
                if (responseText.error) {
                    alert(responseText.error);
                }else{
                    location.reload();
                }
            },
            dataType:  'json',
            timeout:   4000 
        });
    
    
    
    $("#deleteSession-form").ajaxForm({ 
            success:       function(responseText){
                console.log(responseText);
                if (responseText.error) {
                    alert(responseText.error);
                }else{
                    window.location.href = "/classView/";
                }
            },
            dataType:  'json',
            timeout:   4000 
        });
    
    
    
    $(document).on("click", ".addSessionBtn", function(){
        var sessionID = $(this).data('options').sessionID;
        console.log(sessionID);
        var element = $(this);
        if ($(this).html()=='add') {
            var addRemove = 'add';
        }else{
            var addRemove = 'remove';
        }
        
        $.ajax({
            method: "POST",
            url: addSessionURL,
            data: { addRemove: addRemove, sessionID: parseInt(sessionID) },
            dataType: "json",
            timeout: 3000
            })
                .done(function( responseText ) {
                    console.log( responseText );
                    if (responseText.error) {
                        alert(responseText.error);
                    }else{
                        if (element.html()=='add') {
                            element.html('remove').removeClass('btn-sucess').addClass('btn-danger');
                        }else{
                            element.html('add').addClass('btn-sucess').removeClass('btn-danger');
                        }
                    }
            });
    });    
    
    
    
    
    $("#editSession-form input[name=date]").blur(function(){
        console.log($(this).val());
    });
    
    
    
    $("#textLoadbtn").click(function(){
	w = window.open('/class/allSessionsPrint/');
	w.print();
    });
    
    
    $("#mySchedulePrintBtn").click(function(){
	w = window.open('/class/mySchedulePrint/');
	w.print();
    });
    
    
    
    $("#studentPrintbtn").click(function(){
	var studentID = $(this).data("options").studentID;
	w = window.open('/class/mySchedulePrint/'+studentID);
	w.print();
    });
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
});