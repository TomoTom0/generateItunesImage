$("#btn_genImage").on("click", function(){
    const isLargeImage=$("input.check_largeImage").prop("checked");
    const order=3;
    const cssLarge={
    "font-family": "scancardium",
    "font-size": 27*order,
    border: `${4*order}px solid #000000`,
    padding: 25*order,
    width: 100*order,
    margin: 10
  }
    const sepSpace=$("input.check_sepSpace").prop("checked");
    const sep= sepSpace ? " " : "\n" ;
    const inputCodes = $("textarea.inputbox").val().split(sep);
    console.log(inputCodes);
    if (inputCodes.length==0) return;
    const boxArea = $("div.area_cardboxes");
    boxArea.empty();
    for (const inputCode of inputCodes){
      const cardcode=$("<span>", {class:"code"}).append(inputCode);
      const cardbox=$("<div>", {class:"cardbox"}).append(cardcode);
      if (isLargeImage) cardbox.css(cssLarge);
      boxArea.append(cardbox);
      cardbox.css({width:cardcode.width()+4});
    }
    //$("div.area_cardboxes").empty();
  });
  