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

const normal2BScan_map = document.getElementById('normal2BScan_map')
const normal2Bpopup = document.getElementById('normal2Bpopup')
const normal2BPopupContent = document.getElementById('normal2BPopupContent')
const normal2Bpopupcloser = document.getElementById('normal2Bpopupcloser')

const normal2BScanVector = new VectorSource({
	features: new GeoJSON().readFeatures(normal2BScanVectorized_geojson, {
		dataProjection: 'EPSG:3857',
		featureProjection: 'EPSG:3857',
		extractGeometryName: true,
	}),
})

// normal2BScanVectorized visual style
const normal2BScanFeatureStyle = feature => {
	return new Style({
		fill: new Fill({
			color: 'rgb(255, 255, 255)',
		}),
		stroke: new Stroke({
			color: 'rgb(153, 255, 221)',
			width: 2,
		}),
		// text: cellRegionsTextStyle(feature),
	})
}

// normal2BScanVectorized layer
const normal2BScanLayer = new VectorLayer({
	source: normal2BScanVector,
	style: normal2BScanFeatureStyle,
})

// normal2BScanVectorized Overlay
const theOverlay = new Overlay({
	element: normal2Bpopup,
	autoPan: true,
	autoPanAnimation: {
		duration: 250,
	},
})

normal2Bpopupcloser.onclick = () => {
	theOverlay.setPosition(undefined)
	normal2Bpopupcloser.blur()
	return false
}

let expandedAttribution = new Attribution({
	collapsible: false,
})

const normal2BscanMap = new Map({
	controls: defaultControls({ attribution: false }).extend([expandedAttribution, new ZoomSlider()]),
	target: normal2BScan_map,
	layers: [normal2BScanLayer],
	overlays: [theOverlay],
	view: new View({
		maxZoom: 40,
		minZoom: 10,
	}),
})

const mapExtent = normal2BScanLayer.getSource().getExtent()
normal2BscanMap.getView().fit(mapExtent, normal2BscanMap.getSize())

let checkSize = () => {
	let isLess600 = normal2BscanMap.getSize()[0] < 600
	expandedAttribution.setCollapsible(isLess600)
	expandedAttribution.setCollapsed(isLess600)
}
checkSize()
window.addEventListener('resize', checkSize)

// If cell is selected get feature info, don't otherwise
const populate_PopupContent = theFeature => {
	normal2BPopupContent.innerHTML = `
    <p class='text-center'>Name: <span class='text-primary lead'>${theFeature.name}</span></p>
    <a class="btn btn-outline-info my-0" href='/edit-normal2Bscan-vector/${parseInt(theFeature.fid)}'>Edit</a>
    <a class="btn btn-outline-danger my-0" href='/delete-normal2Bscan-vector/${parseInt(theFeature.fid)}'>Delete</a>
    `
}



const singleMapClick = new Select({
	layers: [normal2BScanLayer],
}) //By default, this is module:ol/events/condition~singleClick. Other defaults are exactly what I need

normal2BscanMap.addInteraction(singleMapClick)

let selected = null
normal2BscanMap.on('singleclick', evt => {
	normal2BscanMap.forEachFeatureAtPixel(evt.pixel, layer => {
		selected = layer
	})

	if (selected) {
		let click_coords = evt.coordinate
		theOverlay.setPosition(click_coords)
		populate_PopupContent(selected.getProperties())
		selected = null
	} else {
		theOverlay.setPosition(undefined)
		normal2Bpopupcloser.blur()
	}
})

let attributionComplete = false
normal2BscanMap.on('rendercomplete', () => {
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

sync(normal2BscanMap)
