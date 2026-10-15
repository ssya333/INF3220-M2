// Intro de cheapGPT: ubica la moneda, la marca como vista y la saca al terminar.
// La animación es 100% CSS (intro.css); este script solo la administra.

(function () {
  var intro = document.querySelector(".intro");
  if (!intro) return;

  // Se marca por pestaña: cada pestaña nueva vuelve a mostrar la intro una vez.
  try {
    sessionStorage.setItem("cheapgpt-intro-seen", "1");
  } catch (e) {
    // Sin sessionStorage (modo privado estricto): la intro se repetirá, no pasa nada.
  }

  // Calcula hacia dónde tiene que viajar la moneda para convertirse en la "c":
  // la distancia desde el centro de la pantalla hasta el espacio reservado (.intro-c-slot),
  // y cuánto encogerse para quedar del tamaño de la letra.
  function placeCoin() {
    var slot = intro.querySelector(".intro-c-slot").getBoundingClientRect();
    var coin = intro.querySelector(".intro-coin");
    var size = parseFloat(getComputedStyle(intro).getPropertyValue("--coin"));
    coin.style.setProperty("--dx", (slot.left + slot.width / 2 - window.innerWidth / 2) + "px");
    coin.style.setProperty("--dy", (slot.top + slot.height / 2 - window.innerHeight / 2) + "px");
    coin.style.setProperty("--end-scale", slot.width / size);
  }

  // Se espera a que cargue Inter, para medir el logo con la fuente correcta.
  document.fonts.ready.then(placeCoin);
  window.addEventListener("resize", placeCoin);

  intro.querySelector(".intro-skip").addEventListener("click", function () {
    intro.remove();
  });

  // Apenas empieza a desvanecerse, deja pasar los clicks a la página que ya se ve debajo.
  intro.addEventListener("animationstart", function (event) {
    if (event.target === intro && event.animationName === "intro-fade-out") {
      intro.style.pointerEvents = "none";
    }
  });

  // Cuando termina la intro, se saca de la página.
  intro.addEventListener("animationend", function (event) {
    if (event.animationName === "intro-hide") intro.remove();
  });
})();
