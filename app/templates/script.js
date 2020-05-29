function scorePassword(pass) {
  var wynik = 0;
  var warianty = {
      cyfry: /\d/.test(pass),
      male: /[a-z]/.test(pass),
      duze: /[A-Z]/.test(pass),
      specjalne: /\W/.test(pass),
      dlugosc: pass.length > 7
  };
  for(var war in warianty)
    if(warianty[war] == true) wynik += 100 / 5;

  var color = '';
  
  if(wynik < 50) color ='red';
  else if(wynik > 50 && wynik < 100) color ='yellow';
  else if(wynik == 100) color = 'green';
  $("#strength_score").text(wynik + '%');
  $("#strength_score").css('background-color', color);
  return parseInt(wynik);
}

$(function() {
  $("#password").on("keypress keyup keydown", function() {
      scorePassword($(this).val());
  });
});