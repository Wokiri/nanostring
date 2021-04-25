import 'ol/ol.css'
import GeoJSON from 'ol/format/GeoJSON'
import VectorSource from 'ol/source/Vector'
import { Circle as CircleStyle, Style, Fill, Text, Stroke } from 'ol/style'
import VectorLayer from 'ol/layer/Vector'
import { Map, View } from 'ol'
import Select from 'ol/interaction/Select'
import sync from 'ol-hashed'
import { Attribution, defaults as defaultControls, ZoomSlider } from 'ol/control'

const sampleannotation_map = document.querySelector('#sampleannotation_map')
const mapcontent = document.getElementById('mapcontent')

// sampleAnnotations vector
const sampleAnnotationsVector = new VectorSource({
	features: new GeoJSON().readFeatures(sampleAnnotationsVectorGeoson, {
		dataProjection: 'EPSG:3857',
		featureProjection: 'EPSG:3857',
		extractGeometryName: true,
	}),
})

// sampleAnnotations visual style
const sampleAnnotationsPointStyle = feature => {
	return feature.values_.disease_status === 'DKD'
		? new Style({
				image: new CircleStyle({
					radius: 4,
					fill: new Fill({
						color: 'rgb(204, 0, 0)',
					}),
				}),
		  })
		: new Style({
				image: new CircleStyle({
					radius: 4,
					fill: new Fill({
						color: 'rgb(0, 102, 204)',
					}),
				}),
		  })
}

// sampleAnnotations layer
const sampleAnnotationsLayer = new VectorLayer({
	source: sampleAnnotationsVector,
	style: sampleAnnotationsPointStyle,
})

let expandedAttribution = new Attribution({
	collapsible: false,
})

const sampleAnnotationsMap = new Map({
	controls: defaultControls({ attribution: false }).extend([expandedAttribution, new ZoomSlider()]),
	target: sampleannotation_map,
	layers: [sampleAnnotationsLayer],
	view: new View({
		maxZoom: 20,
		minZoom: 0,
	}),
})

const mapExtent = sampleAnnotationsLayer.getSource().getExtent()
sampleAnnotationsMap.getView().fit(mapExtent, sampleAnnotationsMap.getSize())

let checkSize = () => {
	let isLess600 = sampleAnnotationsMap.getSize()[0] < 600
	expandedAttribution.setCollapsible(isLess600)
	expandedAttribution.setCollapsed(isLess600)
}
checkSize()
window.addEventListener('resize', checkSize)

// sampleAnnotations selection option
const singleMapClick = new Select({
	layers: [sampleAnnotationsLayer],
}) //By default, this is module:ol/events/condition~singleClick. Other defaults are exactly what I need

sampleAnnotationsMap.addInteraction(singleMapClick)

const populate_PopupContent = theFeature => {
	let segmentDisplayName = theFeature.segment_display_name
	let textColor = theFeature.disease_status === 'DKD' ? 'danger' : 'primary'
	let sampleStatus = theFeature.disease_status === 'DKD' ? 'A sickly kidney' : 'A healthy kidney'

	mapcontent.innerHTML = `
      <h4 class="text-center my-2 py-4"><small>Segment Display Name is: </small> ${segmentDisplayName}.</h4>
      <p class="text-${textColor} text-center lead font-weight-bold">${sampleStatus}</p>
      `
}

let selected = null
sampleAnnotationsMap.on('singleclick', evt => {
	sampleAnnotationsMap.forEachFeatureAtPixel(evt.pixel, layer => {
		selected = layer
	})

	if (selected) {
		populate_PopupContent(selected.getProperties())
		selected = null
	} else {
		mapcontent.innerHTML = ''
	}
})

let attributionComplete = false
sampleAnnotationsMap.on('rendercomplete', () => {
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

sync(sampleAnnotationsMap)
