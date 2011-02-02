$(function() {

    var r = $('tr input[id$=order]');
    $(r).each(function(i) {
        r.attr( 'readonly', 'true');
    });

    $( 'tbody'  ).sortable({
        items: 'tr',
        opacity: 0.6,
        handle: 'th',
        update: function(e, ui) {
            $($(this).find('tr').get().reverse()).each(function(i) {
                if ($(this).find('input[id$=order]').val()) {
                    var j =  $(ui.item).find('input[id$=order]').val();
                    if ($(this).find('input[id$=order]').val()) {                   
                        $(this).find('input[id$=order]').val(i+1);
                    }
                }
            });
        }
    });
    $('th').css('cursor', 'move');
});

$(function() {
    $('div.inline-group').sortable({
        /*containment: 'parent',
        zindex: 10, */
        items: 'div.inline-related',
        opacity: 0.6,
        handle: 'h3:first',
        update: function() {
            $(this).find('div.inline-related').each(function(i) {
                if ($(this).find('input[id$=order]').val()) {
                    $(this).find('input[id$=order]').val(i+1);
                }
            });
        }
    });
    $('div.inline-related h3').css('cursor', 'move');
    $('div.inline-related').find('input[id$=order]').parent('div').hide();
});

