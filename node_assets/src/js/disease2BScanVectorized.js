import 'ol/ol.css'
import GeoJSON from 'ol/format/GeoJSON'
import VectorSource from 'ol/source/Vector'
import { Style, Fill, Stroke } from 'ol/style'
import VectorLayer from 'ol/layer/Vector'
import { Map, View } from 'ol'
import Select from 'ol/interaction/Select'
import Overlay from 'ol/Overlay'
import sync from 'ol-hashed'
import { Attribution, defaults as defaultControls, ZoomSlider } from 'ol/control'


const disease2BScan_map = document.getElementById('disease2BScan_map')
const overlay_popup = document.getElementById('popup')
const overlay_content = document.getElementById('popup-content')
const closer = document.getElementById('popup-closer')

// disease2BScanVectorized vector
const disease2BScanVector = new VectorSource({
	features: new GeoJSON().readFeatures(disease2BScanVectorized_geojson, {
		dataProjection: 'EPSG:3857',
		featureProjection: 'EPSG:3857',
		extractGeometryName: true,
	}),
})



const cellsSpatialFeatureStyle = feature => {
	return new Style({
		fill: new Fill({
			color: 'rgb(255, 255, 255)',
		}),
		stroke: new Stroke({
			color: 'rgb(153, 255, 221)',
			width: 2,
		}),
		// text: imageScanTextStyle(feature),
	})
}

// disease2BScanVectorized layer
const disease2BScanLayer = new VectorLayer({
	source: disease2BScanVector,
	style: cellsSpatialFeatureStyle,
})

// disease2BScanVectorized Overlay
const theOverlay = new Overlay({
	element: overlay_popup,
	autoPan: true,
	autoPanAnimation: {
		duration: 250,
	},
})

closer.onclick = () => {
	theOverlay.setPosition(undefined)
	closer.blur()
	return false
}

let expandedAttribution = new Attribution({
	collapsible: false,
})

const disease2bscanMap = new Map({
	controls: defaultControls({ attribution: false }).extend([expandedAttribution, new ZoomSlider()]),
	target: disease2BScan_map,
	layers: [disease2BScanLayer],
	overlays: [theOverlay],
	view: new View({
		maxZoom: 40,
		minZoom: 10,
	}),
})

const mapExtent = disease2BScanLayer.getSource().getExtent()
disease2bscanMap.getView().fit(mapExtent, disease2bscanMap.getSize())

let checkSize = () => {
	let isLess600 = disease2bscanMap.getSize()[0] < 600
	expandedAttribution.setCollapsible(isLess600)
	expandedAttribution.setCollapsed(isLess600)
}
checkSize()
window.addEventListener('resize', checkSize)

// If cell is selected get feature info, don't otherwise
const populate_PopupContent = theFeature => {
	overlay_content.innerHTML = `
    <p class='text-center'>Name: <span class='text-primary lead'>${theFeature.name}</span></p>
    <a class="btn btn-outline-info my-0" href='/edit-disease2bscan-vector/${parseInt(theFeature.fid)}'>Edit</a>
    <a class="btn btn-outline-danger my-0" href='/delete-disease2bscan-vector/${parseInt(theFeature.fid)}'>Delete</a>
    `
}

// Disease2Bscan selection option
const singleMapClick = new Select({
	layers: [disease2BScanLayer],
}) //By default, this is module:ol/events/condition~singleClick. Other defaults are exactly what I need

disease2bscanMap.addInteraction(singleMapClick)

let selected = null
disease2bscanMap.on('singleclick', evt => {
	disease2bscanMap.forEachFeatureAtPixel(evt.pixel, layer => {
		selected = layer
	})

	if (selected) {
		let click_coords = evt.coordinate
		theOverlay.setPosition(click_coords)
		populate_PopupContent(selected.getProperties())
		selected = null
	} else {
		theOverlay.setPosition(undefined)
		closer.blur()
	}
})

let attributionComplete = false
disease2bscanMap.on('rendercomplete', () => {
	if (!attributionComplete) {
		let attribution = document.getElementsByClassName('ol-attribution')[0]
		let attributionList = attribution.getElementsByTagName('ul')[0]
		let firstLayerAttribution = attributionList.getElementsByTagName('li')[0]
		let olAttribution = document.createElement('li')
		olAttribution.innerHTML = '<a href="https://openlayers.org/">OpenLayers Docs</a> &#x2503; '
		let joe_twitter = document.createElement('li')
		joe_twitter.innerHTML = '<a href="https://twitter.com/JWokiri">@JWokiri</a> &#x2503; '
		attributionList.insertBefore(olAttribution, firstLayerAttribution)
		attributionList.insertBefore(joe_twitter, firstLayerAttribution)
		attributionComplete = true
	}
})

sync(disease2bscanMap)
