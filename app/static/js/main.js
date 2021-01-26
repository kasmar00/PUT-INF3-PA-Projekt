// query parameters object
let params = new URLSearchParams();

// getting DOM objects
const starting = document.querySelector("#start");
const ending = document.querySelector("#end");
const alfa = document.querySelector("#alfa");

const kp = document.querySelector("#kp");
const td = document.querySelector("#Td");
const ti = document.querySelector("#Ti");

const area = document.querySelector("#A");
const ca = document.querySelector("#Ca");
const mass = document.querySelector("#m");
const fdmax = document.querySelector("#Fdmax");

const result = document.querySelector("#img");
const submit_b = document.querySelector("#sub");
const reset_b = document.querySelector("#rst");

// query function
const update = (event) => {
  let value = event.target.value;
  if (event.target.id == "start" || event.target.id == "end") {
    value = value / 3.6;
    value = Math.round(value * 1000000) / 1000000;
  }
  params.set(event.target.id, value);
};

// add unique id to each query
params.set("timeId", Date.now()); // for the time being a time from opening a window

// adding event listeners for input DOM objects
starting.addEventListener("change", update);
ending.addEventListener("change", update);
alfa.addEventListener("change", update);

kp.addEventListener("change", update);
td.addEventListener("change", update);
ti.addEventListener("change", update);

area.addEventListener("change", update);
ca.addEventListener("change", update);
mass.addEventListener("change", update);
fdmax.addEventListener("change", update);

// submit function
const submit = () => {
  fetch(`api?${params.toString()}`)
    .then(function (response) {
      return response.json();
    })
    .then(function (item) {
      document.querySelector("#myplot").innerHTML = "";
      Bokeh.embed.embed_item(item, "myplot");
    });
};

// reset function
const reset = () => {
  params = new URLSearchParams();
};

// submit/reset eventlisteners
//submit_b.addEventListener("click", submit);
reset_b.addEventListener("click", reset);

submit(); //display default graph

//podmiana obrazka
jQuery(function(){
    jQuery('#formularz').submit(function(e){
        e.preventDefault();
        submit();//generowanie wykresu
        var vZadana = jQuery('#end').val()
        var nachylenie = jQuery('#alfa').val()
        //console.log('vZadana: '+vZadana)
        //console.log('nachylenie: '+nachylenie)
        if (vZadana < 0 && nachylenie > 0) {
            jQuery('#obrazek').attr('src','/static/pod_gorke_-.jpg')
        } else if (vZadana > 0 && nachylenie > 0)
        {
            jQuery('#obrazek').attr('src','/static/pod_gorke_+.jpg')
        }
        else if (vZadana > 0 && nachylenie < 0)
        {
            jQuery('#obrazek').attr('src','/static/z_gorki_+.png')
        }
        else if (vZadana < 0 && nachylenie < 0)
        {
            jQuery('#obrazek').attr('src','/static/z_gorki_-.jpg')
        }
    })
})
