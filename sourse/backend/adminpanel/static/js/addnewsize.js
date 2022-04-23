/*
* Identifier for debug mode(if true - form submited on server)
* */
var is_validate_js = true;
$.validator.setDefaults( {
			submitHandler: function () {
			    if (is_validate_js){
			    	$( "#add_new_size" ).submit();
                }
     		}
		} );
$(document).ready(function () {
//Validations form

    $( "#add_new_size" ).validate( {
				rules: {
                    age: {
                        required: true,
                        maxlength: 10
                    },
                    height: {
                        required: true,
                        maxlength: 10,
                        number: true
                    },
                    chest: {
                        required: true,
                        maxlength: 10,
                        number: true
                    },
                    waist: {
                        required: true,
                        maxlength: 10,
                        number: true
                    }
                },
				messages: {
					age: {
						required: "Пожалуйста введите возраст",
						maxlength: "Не более 10 символов"
					},
					height: {
						required: "Пожалуйста введите рост",
						maxlength: "Не более 10 символов",
                        number: "Должно быть числом"
					},
					chest: {
						required: "Пожалуйста введите обхват груди",
						maxlength: "Не более 10 символов",
                        number: "Должно быть числом"
					},
                    waist: {
					   maxlength: "Не более 10 символов",
                       required: "Пожалуйста введите обхват талии",
                       number: "Должно быть числом"
					}
				},
				 //errorElement: "em",
				// errorPlacement: function ( error, element ) {
				// 	// Add the `help-block` class to the error element
				// 	error.addClass( "help-block" );
                //
				// 	// Add `has-feedback` class to the parent div.form-group
				// 	// in order to add icons to inputs
				// 	element.parents( ".form-group" ).addClass( "has-feedback" );
                //
				// 	if ( element.prop( "type" ) === "checkbox" ) {
				// 		error.insertBefore( element.parent( "label" ) );
				// 	} else {
				// 		error.insertBefore( element );
				// 	}
                //
				// 	// Add the span element, if doesn't exists, and apply the icon classes to it.
				// 	if ( !element.next( "span" )[ 0 ] ) {
				// 		$( "<span class='glyphicon glyphicon-remove form-control-feedback'></span>" ).insertBefore( element );
				// 	}
				// },
				// success: function ( label, element ) {
				// 	// Add the span element, if doesn't exists, and apply the icon classes to it.
				// 	if ( !$( element ).next( "span" )[ 0 ] ) {
				// 		$( "<span class='glyphicon glyphicon-ok form-control-feedback'></span>" ).insertBefore( $( element ) );
				// 	}
				// },
				highlight: function ( element, errorClass, validClass ) {
					$( element ).parents( ".form-group" ).addClass( "has-error" ).removeClass( "has-success" );
					$( element ).next( "em" ).addClass( "glyphicon-remove" ).removeClass( "glyphicon-ok" );
				},
				unhighlight: function ( element, errorClass, validClass ) {
					$( element ).parents( ".form-group" ).addClass( "has-success" ).removeClass( "has-error" );
					$( element ).next( "em" ).addClass( "glyphicon-ok" ).removeClass( "glyphicon-remove" );
				}
			} );
});