$.ajaxSetup({
    headers: {
        "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
    }
    })
var responseForm = $('.response_form')
responseForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this)
    var actionEndpoint = thisForm.attr('action')
    var httpMethod = thisForm.attr('method')
    var formData = thisForm.serialize()
    $.ajax({
        method: httpMethod,
        url: actionEndpoint,
        data: formData,
        success: function(data){
            console.log('success', data)
            var response_button = thisForm.find('.response-button')
            if (data['created'] === true){
                response_button.html("<button class='responded btn btn-outline-dark' type='submit'>Responded</button>")
                response_button.find('button').mouseover(function(){
                    $(this).text('Cancel')
                })
                response_button.find('button').mouseout(function(){
                    $(this).text('Responded')
                })
            } else if (data['created'] == false){
                response_button.html("<button class='respond mybtn btn btn-success' type='submit'>Respond</button>")
            }
        },
        error: function(error){
            console.log(error)
        }
    })
})
var responded = $('.responded')
responded.mouseover(function(){
    $(this).text('Cancel')
})
responded.mouseout(function(){
    $(this).text('Responded')
})
