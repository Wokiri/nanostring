import "ol/ol.css";
import GeoJSON from "ol/format/GeoJSON";
import VectorSource from "ol/source/Vector";
import { Style, Fill, Text, Stroke } from "ol/style";
import VectorLayer from "ol/layer/Vector";
import { Map, View } from "ol";
import sync from "ol-hashed";

const issuesmap = document.querySelector("#issuesmap");

// This json files were used for testing during dev mode. The actual app fetches these from a database
// const issuescountiesjson = require("./issuescounties.json");

const issuescountiesVector = new VectorSource({
  features: new GeoJSON().readFeatures(issuescountiesjson, {
    extractGeometryName: true,
  }),
});


const issuescountiesTextLabel = (feature) => `${feature.get("name")}`;

const issuescountiesTextStyle = (feature) =>
  new Text({
    textAlign: "center",
    textBaseline: "middle",
    font: `light 14px "Trebuchet MS", Helvetica, sans-serif`,
    text: issuescountiesTextLabel(feature),
    placement: "polygon",
    fill: new Fill({
      color: "rgb(0, 51, 51)",
    }),
  });

const issuescountiesPolygonStyle = (feature) => {
  return new Style({
    fill: new Fill({
      color: "rgb(230, 255, 255)",
    }),
    stroke: new Stroke({
      color: "rgb(0, 51, 51)",
      width: 1,
    }),
    text: issuescountiesTextStyle(feature),
  });
};

// counties layer
const countiesLayer = new VectorLayer({
  source: issuescountiesVector,
  style: issuescountiesPolygonStyle,
});


const locationDemoMap = new Map({
  target: issuesmap,
  layers: [countiesLayer],
  view: new View({
    center: [36.8166667, -1.2833333],
    zoom: 24,
  }),
});

sync(locationDemoMap);
