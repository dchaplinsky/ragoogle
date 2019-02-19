document.addEventListener(
  "touchstart",
  function () {
  },
  true
);

$(function () {
  $("[data-toggle=popover]").popover({
    html: true
  });

  $(".small-profile ").hover(
    function () {
      $(this).addClass('hovered');
      $(this).closest('.row').addClass('hovered');
    }, function () {
      $(this).removeClass('hovered');
      $(this).closest('.row').removeClass('hovered');
    }
  );

  $("#clearall").click(function () {
    $(this).closest('.form-group').find('.custom-control-input').prop('checked', $(this).prop('checked'));
  });
});
