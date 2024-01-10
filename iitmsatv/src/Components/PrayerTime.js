import React, { Component } from 'react'
import FajrPic from "../images/PrayerTimeIcons/Fajr-Isha.png"
import SunrisePic from "../images/PrayerTimeIcons/Sunrise.png"
import DhuhrPic from "../images/PrayerTimeIcons/Dhuhr.png"
import AsrPic from "../images/PrayerTimeIcons/Asr.png"
import MaghribPic from "../images/PrayerTimeIcons/Maghrib.png"
import IshaPic from "../images/PrayerTimeIcons/Fajr-Isha.png"

class PrayerTime extends Component {

    constructor(props) {
        super(props)
    
        this.picsize = "70px"; //Size of the image for this prayer card
    }

    formatTime(time){
        var newTime = `${time}`;    //Quick way to create full copy of 'time'. Can't use var newTime = time; Because that causes newtime -> time which would modify 'time' directly. We don't want that we want a full copy of 'time'
        for (const phrase of ['CDT', 'CST', '()']) {
            newTime = newTime.replace(phrase,'');
        }

        if(newTime.length === 0){
            return newTime;
        }

        var hour = parseInt(time.substring(0,2));
        if(hour > 12){
            hour -= 12;
            newTime = hour.toString() + newTime.substring(2) + ' PM';
        }
        else if (hour === 12){
            newTime = newTime + ' PM';
        }
        else if (hour < 10) {
            newTime = hour.toString() + newTime.substring(2) + ' AM';
        }
        else{
            newTime = newTime + ' AM';
        }
        // console.log("new time: " + newTime);
        return newTime;
    }
    
    getPhotoPath(prayer) {
        if (prayer === 'Fajr'){
            return FajrPic;
        }
        else if(prayer === 'Sunrise'){
            return SunrisePic;
        }
        else if(prayer === 'Dhuhr'){
            return DhuhrPic;
        }
        else if(prayer === 'Asr'){
            return AsrPic;
        }
        else if(prayer === 'Maghrib'){
            return MaghribPic;
        }
        else if(prayer === 'Isha'){
            return IshaPic;
        }
    }

    render() {
        return (
            <div id='PrayerCard'>
                <div>
                    <label>{this.formatTime(this.props.start)}</label>
                </div>
                <div>
                    <label>{this.props.prayer}</label>
                </div>
                <img    src={this.getPhotoPath(this.props.prayer)} 
                            alt={this.props.prayer}
                            style={{ width: this.picsize, height: this.picsize, objectFit: 'cover' }}
                    ></img>
                <div>
                    <label style={{fontSize: '40px' }}>{this.formatTime(this.props.iqamah)}</label>
                </div>
            </div>
        )
    }
}

export default PrayerTime