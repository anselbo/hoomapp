// var cleave = new Cleave(".goo", {
//   numeral: true,
//   numeralThousandsGroupStyle: "thousand",
// });

$(document).ready(function () {
  var date_input = $('input[name="due"]');
  var options = {
    dateFormat: "yy-mm-dd",
  };
  date_input.datepicker(options);
});


