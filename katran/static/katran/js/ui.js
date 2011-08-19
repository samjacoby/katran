$(function($) {
  $("form").sortable({
    item: '.family',
    opacity: 0.6,
    cursor: "move",
    axis: 'y',
    update: function(e, ui) {
              $.ajax({
                url: "/dashboard/action/",
                type: "POST",
                data: ({ 
                  id: $(ui.item).attr('id').replace(/[^\d]+/g, ''), 
                  action: 'family',
                  order: $(ui.item).prevAll('form .family').length,
                  }),
                success: function(msg) { 
                  msg = $('<span class="msg">Order updated.</span>').delay(3000).fadeOut('slow'); 
                  $('#top-menu').append(msg);
                }
              })            
            }
  });

  $(".stamp-family").sortable({
    item: '.stamp',
    opacity: 0.6,
    cursor: "move",
    axis: 'y',
    update: function(e, ui) {
              $.ajax({
                url: "/dashboard/action/",
                type: "POST",
                data: ({ 
                  action: 'stamp',
                  id: $(ui.item).attr('id').replace(/[^\d]+/g, ''), 
                  order: $(ui.item).prevAll('.stamp-family .stamp').length,
                  }),
                success: function(msg) { 
                  msg = $('<span class="msg">Order updated.</span>').delay(3000).fadeOut('slow'); 
                  $('#top-menu').append(msg);
                }
              })            
            }
  });
})

