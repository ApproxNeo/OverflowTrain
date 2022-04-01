SIGTrain();

function SIGTrain() {
  startupAnimation();
  enableMapDragging();
  enableStationClicking();
}

function startupAnimation() {
  $("body").hide().fadeIn(900);

  $(".station").addClass("animated heartBeat infinite");
}

function enableMapDragging() {
  document.addEventListener("touchstart", touchHandler, true);
  document.addEventListener("touchmove", touchHandler, true);
  document.addEventListener("touchend", touchHandler, true);
  document.addEventListener("touchcancel", touchHandler, true);

  $("#map").draggable();

  // Cursor CSS Property change
  $("#map").on("mousedown touchstart", function (evt) {
    $("#map").css("cursor", "grabbing");
  });

  $("#map").on("mouseup touchend", function (evt) {
    $("#map").css("cursor", "grab");
  });
}

function touchHandler(event) {
  var touch = event.changedTouches[0];

  var simulatedEvent = document.createEvent("MouseEvent");
  simulatedEvent.initMouseEvent(
    {
      touchstart: "mousedown",
      touchmove: "mousemove",
      touchend: "mouseup",
    }[event.type],
    true,
    true,
    window,
    1,
    touch.screenX,
    touch.screenY,
    touch.clientX,
    touch.clientY,
    false,
    false,
    false,
    false,
    0,
    null
  );

  touch.target.dispatchEvent(simulatedEvent);
  event.preventDefault();
}

function enableStationClicking() {
  $(".station").on("mousedown", (evt) => {
    var station = convertUnderscore(
      evt.target.className.substr(8).split(" ")[0]
    );

    console.log(station);

    var xhr = new XMLHttpRequest();
    var url = "/api/orders/add";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({ destination: station });
    console.log(data);
    xhr.send(data);
  });
}

function convertUnderscore(string) {
  return string.replace(/_/g, " ");
}
