function init() {
    // initialize with power graph
    //document.getElementsById("pt-graph").innerHTML = powerLink;
    showPower();
    showLegPower();
    groupRares();
}

init();

function showPower() {
    document.getElementById("power-graph").style.display = "block";
    document.getElementById("toughness-graph").style.display = "none";
}

function showToughness() {
    document.getElementById("toughness-graph").style.display = "block";
    document.getElementById("power-graph").style.display = "none";
}

function showLegPower() {
    document.getElementById("leg-power-graph").style.display = "block";
    document.getElementById("leg-toughness-graph").style.display = "none";
}

function showLegToughness() {
    document.getElementById("leg-toughness-graph").style.display = "block";
    document.getElementById("leg-power-graph").style.display = "none";
}

function groupRares() {
    document.getElementById("group-rares-graph").style.display = "block";
    document.getElementById("split-rares-graph").style.display = "none";
}

function splitRares() {
    document.getElementById("split-rares-graph").style.display = "block";
    document.getElementById("group-rares-graph").style.display = "none";
}