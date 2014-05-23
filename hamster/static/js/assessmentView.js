var data= [
   {
      "productId":1,
      "name":"COS301",
      "Mark":1,
      "productoption":[
         {
            "productOptionId":2,
            "topping":"Semester test",
            "Mark":0.50
	 },
         {
            "productOptionId":3,
            "topping":"Projects",
            "Weight":0.50
         }
      ]
   },
   {
      "productId":2,
      "name":"COS222",
      "Mark":1,
      "productoption":[
         {
            "productOptionId":4,
            "topping":"Practicals",
            "Weight":0.50
         },
         {
            "productOptionId":5,
            "topping":"Semester test",
            "Weight":0.50
         }
      ],
     
      
   }
];

function createList(menudata){
    var html = '';
    $.each(menudata,function(i,val){
        html += '<div data-role="collapsible" data-inset="true" data-id='+val.productId+'><h3>'+val.name+'</h3><ul data-role="listview" data-inset="true">';
        $.each(val.productoption,function(i,val){
            html += '<li class="row" onclick="loadPage()">'+val.topping+'</li>';
        });
        html += '</ul></div>';
    });
    return html;
}

$(document).ready( function () {
    var menulistitem = createList(data);
    $('#menu-content').empty().append(menulistitem);
    $('div[data-role=collapsible]').collapsible();
    $('div ul').listview();
});
/*
function loadPage()
{
    window.location.href="/assessmentManager/";
}*/


/*function load()
{
    document.getElementById("menu-content").innerHTML = "test";
}*/