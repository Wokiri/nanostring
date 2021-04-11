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

const cellSpatial_map = document.getElementById("cell_spatial_map");
const overlay_popup = document.getElementById("popup");
const overlay_content = document.getElementById("popup-content");
const closer = document.getElementById("popup-closer");


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
      color: "rgb(153, 221, 255)",
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
    center: [mapLon, mapLat],
    zoom: 28,
  }),
});

cellsSpatialMap.addControl(new ZoomSlider());

// sampleAnnotations selection option
const singleMapClick = new Select({
  layers: [cellsSpatialLayer],
}); //By default, this is module:ol/events/condition~singleClick. Other defaults are exactly what I need

cellsSpatialMap.addInteraction(singleMapClick);

cellsSpatialMap.on("singleclick", (evt) => {
  let click_coords = evt.coordinate;
  overlay_content.innerHTML = `<p>${click_coords}</p>`;
  theOverlay.setPosition(click_coords);
  console.log(click_coords);
});

sync(cellsSpatialMap);
