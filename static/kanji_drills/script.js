$(function () {

    var isToggle = function() {
        return $("a.kj-on-off-toggle").data('toggle');
    }

    var isMouseOver = function() {
        return $(".kj-mouseover-toggle").is(':checked');
    }

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

            if (e.ctrlKey) {

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

    $(".kj-subsection .kj-reading").addClass("invisible");
    $(".kj-subsection .kj-meaning").addClass("invisible");

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

    $("a.kj-random")
        .click(function (e) {
            var kanji = $(".kj-container .kj-element").detach().toArray();
            var newOrder = _.shuffle(kanji);
            $(".kj-grid").append(newOrder);

        });

    $(".kj-mouseover-toggle")
        .prop('checked', false);

});