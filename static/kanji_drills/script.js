$(function () {

    var isToggle = function() {
        return $("a.kj-on-off-toggle").data('toggle');
    }

    var isMouseOVer = function() {
        return $(".kj-mouseover-toggle").is(':checked');
    }

    $(".kj-element")
        .mouseover(function () {
            var toggle = isToggle();
            var mouseover = isMouseOVer();
            if (toggle || !mouseover) return;

            $(this).find(".kj-reading").removeClass("invisible");
            $(this).find(".kj-meaning").removeClass("invisible");
        })
        .mouseleave(function () {
            var toggle = isToggle();
            var mouseover = isMouseOVer();
            if (toggle || !mouseover) return;

            $(this).find(".kj-reading").addClass("invisible");
            $(this).find(".kj-meaning").addClass("invisible");
        })
        .click(function() {
            var mouseover = isMouseOVer();
            if (mouseover) return;

            if ($(this).find(".kj-reading").hasClass('invisible')) {
                $(this).find(".kj-reading").removeClass("invisible");
                $(this).find(".kj-meaning").removeClass("invisible");
            } else {
                $(this).find(".kj-reading").addClass("invisible");
                $(this).find(".kj-meaning").addClass("invisible");
            }
        });

    $(".kj-subsection .kj-reading").addClass("invisible");
    $(".kj-subsection .kj-meaning").addClass("invisible");

    $("a.kj-on-off-toggle")
        .data('toggle', false)
        .click(function() {
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

    $("a.kj-random")
        .click(function () {
            var kanji = $(".kj-container .kj-element").detach().toArray();
            var newOrder = _.shuffle(kanji);
            $(".kj-grid").append(newOrder);

        });

    $(".kj-mouseover-toggle")
        .prop('checked', false);

});