const roundoff = (num, dp) => Number(Math.round(num + 'e' + dp) + 'e-' + dp)
const pad = num => num < 10 ? "0" + num : num
const posneg = num => num < 0 ? num : "+" + num

const mapTime = timezoneOffset => {

    const days_of_the_week = ['Sunday', 'Monday', 'Tuesday', 'Wednessday', 'Thursday', 'Friday', 'Saturday']

    let D = new Date()
    let day = D.getDay()
    let hours = D.getHours()
    let minutes = D.getMinutes()
    let seconds = D.getSeconds()
    let localTimezone = -1 * (D.getTimezoneOffset()) / 60

    let mapTimezoneSeconds, totalmapminutes, mapminutes, mapseconds, maphours, theDay

    if (timezoneOffset >= localTimezone) {

        mapTimezoneSeconds = (timezoneOffset - localTimezone) * 3600
        mapseconds = (seconds + mapTimezoneSeconds) % 60

        totalmapminutes = minutes + (((seconds + mapTimezoneSeconds) - mapseconds) / 60)
        mapminutes = totalmapminutes % 60

        maphours = hours + ((totalmapminutes - mapminutes) / 60)

        if (maphours >= 24) {
            day += 1
            maphours -= 24
            day = (day > 6) ? day - 7 : day
        }

    } else {

        mapTimezoneSeconds = (localTimezone - timezoneOffset) * 3600

        maphours = hours - ((mapTimezoneSeconds / 3600) - (mapTimezoneSeconds % 3600) / 3600)

        if (maphours < 0) {
            day -= 1
            maphours += 24
            day = (day < 0) ? day + 7 : day
        }

        totalmapminutes = minutes - ((mapTimezoneSeconds % 3600) / 3600) * 60
        mapminutes = totalmapminutes % 60

        mapseconds = seconds
    }

    theDay = days_of_the_week[day]

    return {
        D: theDay,
        H: pad(maphours),
        M: pad(mapminutes),
        S: pad(mapseconds)
    }

}

export {
    roundoff,
    pad,
    posneg,
    mapTime
}