$(function () {

    function getParams() {
        // gets url parameters and builds an object
        return _.chain(location.search.slice(1).split('&'))
            .map(function (item) { if (item) { return item.split('='); } })
            .compact()
            .fromPairs()
            .value();
    }

    function isToggle() {
        return $("a.kj-on-off-toggle").data('toggle');
    }

    function isMouseOver() {
        return $(".kj-mouseover-toggle").is(':checked');
    }

    // KANJI BEHAVIOUR

    $(".kj-element")
        .mouseover(function () {
            var toggle = isToggle();
            var mouseover = isMouseOver();
            if (toggle || !mouseover) return;

            $(this).find(".kj-reading").removeClass("invisible");
            $(this).find(".kj-meaning").removeClass("invisible");
        })
        .mouseleave(function () {
            var toggle = isToggle();
            var mouseover = isMouseOver();
            if (toggle || !mouseover) return;

            $(this).find(".kj-reading").addClass("invisible");
            $(this).find(".kj-meaning").addClass("invisible");
        })
        .click(function(e) {
            var mouseover = isMouseOver();
            if (mouseover) return;

            if (e.ctrlKey || e.metaKey) {

                // Toggle selection
                if ($(this).closest(".kj-element").hasClass('kj-element-selected')) {
                    $(this).closest(".kj-element").removeClass("kj-element-selected");
                } else {
                    $(this).closest(".kj-element").addClass("kj-element-selected");
                }

            } else {

                // Toggle the definition
                if ($(this).find(".kj-reading").hasClass('invisible')) {
                    $(this).find(".kj-reading").removeClass("invisible");
                    $(this).find(".kj-meaning").removeClass("invisible");
                } else {
                    $(this).find(".kj-reading").addClass("invisible");
                    $(this).find(".kj-meaning").addClass("invisible");
                }

            }
        });

    // ON/OFF BEHAVIOUR

    $("a.kj-on-off-toggle")
        .data('toggle', false)
        .click(function(e) {
            var toggle = isToggle();

            if (!toggle) {
                $(".kj-subsection .kj-reading").removeClass("invisible");
                $(".kj-subsection .kj-meaning").removeClass("invisible");
            } else {
                $(".kj-subsection .kj-reading").addClass("invisible");
                $(".kj-subsection .kj-meaning").addClass("invisible");
            }

            $(this).data('toggle', !toggle);
        });

    // SHOW/HIDE BEHAVIOUR

    $("a.kj-show-hide-toggle")
        .data('toggle', false)
        .click(function() {
            var toggle = $(this).data('toggle');
            console.log(toggle);

            if (toggle) {
                $(".kj-element").not(".kj-element-selected").show();
            } else {
                $(".kj-element").not(".kj-element-selected").hide();
            }

            $(this).data('toggle', !toggle);
        });

    // RAND BEHAVIOUR

    $("a.kj-random")
        .click(function (e) {
            var kanji = $(".kj-container .kj-element").detach().toArray();
            var newOrder = _.shuffle(kanji);
            $(".kj-grid").append(newOrder);

        });

    // ADVANCED MODAL BEHAVIOUR

    $(".kj-show-advanced-modal")
        .click(function() {
            var params = getParams();

            $('#adv-level').val(params['level'] || 1);
            $('#adv-size').val(params['size'] || 50);
            $('#adv-only').val(decodeURI(params['only'] || ''));

            $("#advancedModal").modal("show");
        });

    $(".kj-get-selected")
        .click(function() {
            $('#adv-only').val(
                $(".kj-element.kj-element-selected .kj-character").text()
            );
        });

    $(".kj-advanced-go")
        .click(function() {

            var token = getParams()['token'];

            var level = $('#adv-level').val();
            var size = $('#adv-size').val();
            var only = $('#adv-only').val();

            location.search = '?token=' + token +
                '&level=' + level +
                '&size=' + size +
                '&only=' + only;

            $("#advancedModal").modal("hide");
        });



    // MOUSEOVER BEHAVIOUR

    $(".kj-mouseover-toggle")
        .prop('checked', false);

});