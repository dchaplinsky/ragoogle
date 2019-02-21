$(function() {
    $(".search-form-q").typeahead({
        minLength: 2,
        items: 100,
        autoSelect: false,
        source: function(query, process) {
            $.get($(".search-form-q").data("endpoint"),
                this.$element.closest("form").find("input").serialize())
                .done(function(data) {
                    process(data);

                    $("a.autocomplete-hint").on("click", function(e) {
                        e.stopPropagation();
                    });
                })
        },
        matcher: function() {
            return true;
        },
        highlighter: function(instance) {
        	return instance;
        },
        updater: function(instance) {
            return $(instance).data("sugg_text")
        },
        afterSelect: function(item) {
            var form = $(".search-form-q").closest("form");
            form.find("input[name=is_exact]").val("on");

            form.submit();
        }
    });
});
