$(document).ready(function(){
	$('#block-error').hide();
	$('#search').autocomplete({
	    serviceUrl: '/searchjson/',
	    minChars: 2, // Минимальная длина запроса для срабатывания автозаполнения
	    delimiter: /(,|;)\s*/, // Разделитель для нескольких запросов, символ или регулярное выражение
	    maxHeight: 400, 
	    params: { model:{'0':'Author','1':'Book'} },	
	    width: 300, 
	    zIndex: 9999, 
	    deferRequestBy: 300,
 	    noCache:false,
	    onSelect: function(data, value){ },
     	    onSearchStart:function(query){$(this).addClass("ui-autocomplete-loading")},
    	    onSearchComplete:function(query){$(this).removeClass("ui-autocomplete-loading")}
	});
	$('#authors').autocomplete({
	    serviceUrl: '/searchjson/',
	    minChars: 2, // Минимальная длина запроса для срабатывания автозаполнения
	    delimiter: /(,|;)\s*/, // Разделитель для нескольких запросов, символ или регулярное выражение
	    params: { model:{'0':'Author'}},	
	    maxHeight: 400, 
	    width: 300, 
	    zIndex: 9999, 
	    deferRequestBy: 300,
 	    noCache:false,
	    onSelect: function(data, value){ },
     	    onSearchStart:function(query){$(this).addClass("ui-autocomplete-loading")},
    	    onSearchComplete:function(query){$(this).removeClass("ui-autocomplete-loading")}
	});
     $('.edit').editable("/admin/ajax/save/", {
         indicator : 'Saving...',
         tooltip   : 'Click to edit...',
	 cancel    : '<img class=edit-icons src="/static/icon_error.gif">',
         submit    : '<img class=edit-icons src="/static/icon_success.gif">',
         indicator : '<img class=edit-icons src="/static/progress.gif">',
	 style	   : 'table-row',
	 width	   : 'none',
	 submitdata: function(value, settings) { 
		 		name = $(this).attr('name')
			 	return {'name': name};},
	 onerror : function(settings,original,xhr){
				$('#error').html(xhr.responseText)
				$('#block-error').show()
				original.reset();},
     });
});
