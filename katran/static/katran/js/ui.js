$(function($) {
  $("ul.families" ).sortable({
    item: 'div',
    opacity: 0.6,
    cursor: "move",
    update: function(e, ui) {
              $.ajax({
                url: "/dashboard/action/",
                type: "POST",
                data: ({ 
                  id: $(ui.item).attr('id').replace(/[^\d]+/g, ''), 
                  action: 'family',
                  order: $(ui.item).prevAll().length,
                  }),
                success: function(msg) { 
                  alert(msg)
                }
              })            
            }
  });

  $("ul.family" ).sortable({
    item: 'li',
    opacity: 0.6,
    cursor: "move",
    update: function(e, ui) {
              $.ajax({
                url: "/dashboard/action/",
                type: "POST",
                data: ({ 
                  action: 'stamp',
                  id: $(ui.item).attr('id').replace(/[^\d]+/g, ''), 
                  order: $(ui.item).prevAll().length,
                  }),
                success: function(msg) { 
                  alert(msg)
                }
              })            
            }
  });
})

