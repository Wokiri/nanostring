import "ol/ol.css";
import GeoJSON from "ol/format/GeoJSON";
import VectorSource from "ol/source/Vector";
import { Circle as Style, Fill, Stroke } from "ol/style";
import VectorLayer from "ol/layer/Vector";
import { Map, View } from "ol";
import Select from "ol/interaction/Select";
import sync from "ol-hashed";

import ZoomSlider from "ol/control/ZoomSlider";

const cellSpatial_map = document.querySelector("#cell_spatial_map");
// const mapcontent = document.getElementById("mapcontent");

const cell_spatial_geojson = require("./test.json");

const cellsSpatialVector = new VectorSource({
  features: new GeoJSON().readFeatures(cell_spatial_geojson, {
    extractGeometryName: true,
  }),
});

// cellsSpatial visual style
const cellsSpatialFeatureStyle = (feature) => {
  return new Style({
    fill: new Fill({
      color: "rgba(102, 102, 204, 1)",
    }),
    stroke: new Stroke({
      color: "rgb(217, 217, 242)",
      width: 2,
    }),
    // text: regionsTextStyle(feature),
  });
};

// cellsSpatial layer
const cellsSpatialLayer = new VectorLayer({
  source: cellsSpatialVector,
  style: cellsSpatialFeatureStyle,
});

const cellsSpatialMap = new Map({
  target: cellSpatial_map,
  layers: [cellsSpatialLayer],
  view: new View({
    center: [0.0, 1.6],
    zoom: 28,
  }),
  //   view: new View({
  //     center: [mapLon, mapLat],
  //     zoom: mapZoom,
  //   }),
});

cellsSpatialMap.addControl(new ZoomSlider());

// sampleAnnotations selection option
const singleMapClick = new Select({
  layers: [cellsSpatialLayer],
}); //By default, this is module:ol/events/condition~singleClick. Other defaults are exactly what I need


cellsSpatialMap.addInteraction(singleMapClick);

sync(cellsSpatialMap);
