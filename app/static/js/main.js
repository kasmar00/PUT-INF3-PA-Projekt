// query parameters object
const params = new URLSearchParams();

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

// query function
const update = (event) => {
  params.set(event.target.id, event.target.value);
  result.src = `api?${params.toString()}`;
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
