import "ol/ol.css";
import GeoJSON from "ol/format/GeoJSON";
import VectorSource from "ol/source/Vector";
import { Style, Fill, Text, Stroke } from "ol/style";
import VectorLayer from "ol/layer/Vector";
import { Map, View } from "ol";
import Select from "ol/interaction/Select";
import Overlay from "ol/Overlay";
import sync from "ol-hashed";
import ZoomSlider from "ol/control/ZoomSlider";

import { geo_webMercator, roundoff } from "./parameters";

const cellSpatial_map = document.getElementById("cell_spatial_map");
const overlay_popup = document.getElementById("popup");
const overlay_content = document.getElementById("popup-content");
const closer = document.getElementById("popup-closer");

const cell_spatial_geojson = require("./test.json");

const cellRegionsTextLabel = (feature) => feature.get("name");

const cellRegionsTextStyle = (feature) =>
  new Text({
    textAlign: "center",
    textBaseline: "middle",
    font: `bold 14px "Trebuchet MS", Helvetica, sans-serif`,
    text: cellRegionsTextLabel(feature),
    placement: "polygon",
    fill: new Fill({
      color: "rgb(25, 25, 77)",
    }),
  });

const cellsSpatialVector = new VectorSource({
  features: new GeoJSON().readFeatures(cell_spatial_geojson, {
    extractGeometryName: true,
  }),
});

// cellsSpatial visual style
const cellsSpatialFeatureStyle = (feature) => {
  return new Style({
    fill: new Fill({
      color: "rgb(255, 255, 255)",
    }),
    stroke: new Stroke({
      color: "rgb(153, 255, 221)",
      width: 2,
    }),
    text: cellRegionsTextStyle(feature),
  });
};

// cellsSpatial layer
const cellsSpatialLayer = new VectorLayer({
  source: cellsSpatialVector,
  style: cellsSpatialFeatureStyle,
});

const theOverlay = new Overlay({
  element: overlay_popup,
  autoPan: true,
  autoPanAnimation: {
    duration: 250,
  },
});

closer.onclick = () => {
  theOverlay.setPosition(undefined);
  closer.blur();
  return false;
};

const cellsSpatialMap = new Map({
  target: cellSpatial_map,
  layers: [cellsSpatialLayer],
  overlays: [theOverlay],
  view: new View({
    center: [parseFloat(77.31375), parseFloat(-49.4071)],
    zoom: 28,
  }),
  //   view: new View({
  //     center: [mapLon, mapLat],
  //     zoom: 28,
  //   }),
});

cellsSpatialMap.addControl(new ZoomSlider());

// If region is selected get feature info, don't otherwise
const bringLayerPopupInfo = (theFeature) => {
  let layerAttributes = theFeature.getFeatures().array_[0];
  

  if(layerAttributes){
    overlay_content.innerHTML = `
    <p class='text-center text-primary'>${layerAttributes.values_.name}</p>
    <a class="btn btn-outline-info my-0" href='/edit-cells/${layerAttributes.values_.fid}'>Edit</a>
    <a class="btn btn-outline-danger my-0" href='/delete-cells/${layerAttributes.values_.fid}'>Delete</a>
    `;
  }

  
};

// sampleAnnotations selection option
const singleMapClick = new Select({
  layers: [cellsSpatialLayer],
}); //By default, this is module:ol/events/condition~singleClick. Other defaults are exactly what I need

cellsSpatialMap.addInteraction(singleMapClick);

singleMapClick.on("select", (elem) => {
  bringLayerPopupInfo(elem.target);
  
});

cellsSpatialMap.on("singleclick", (evt) => {
  let click_coords = evt.coordinate;
  theOverlay.setPosition(click_coords);
  let lon = click_coords[0];
  let lat = click_coords[1];
  let coords_webmercator = geo_webMercator(lon, lat);
  let x_coords = coords_webmercator[0] / 1000; // I had georeferenced the image by expanding extents by 1000
  let y_coords = coords_webmercator[1] / 1000;
  overlay_content.innerHTML = `<p>${roundoff(x_coords, 2)}, ${roundoff(y_coords, 2)}</p>`;
});

sync(cellsSpatialMap);
