$(function($) {
  $(".designer" ).sortable({
    item: 'ul',
    opacity: 0.6,
    cursor: "move",
    containment: 'parent',
    axis: 'y',
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

  $(".family" ).sortable({
    item: 'li',
    opacity: 0.6,
    cursor: "move",
    axis: 'y',
    containment: 'parent',
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

