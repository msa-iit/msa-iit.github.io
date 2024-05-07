import React, { Component } from 'react'
import FajrPic from "../images/PrayerTimeIcons/Fajr-Isha.png"
import SunrisePic from "../images/PrayerTimeIcons/Sunrise.png"
import DhuhrPic from "../images/PrayerTimeIcons/Dhuhr.png"
import AsrPic from "../images/PrayerTimeIcons/Asr.png"
import MaghribPic from "../images/PrayerTimeIcons/Maghrib.png"
import IshaPic from "../images/PrayerTimeIcons/Fajr-Isha.png"

/*
Displays the countdown until next Salah

Parameters passed from Parent
- salah: The next Salah that is being counted down to
- type:     time: the 'finish_time' passed in is for actual start of the time for prayer (Usually comes before the iqamah)
            iqamah: the 'finish_time' passed in is for the iqamah
            khutbah: the 'finish_time' passed in is for the jummah khutbah time
- finish_time: The time that the countdown will end at
- callback: function located in the Parent Component to fetch the next prayer time after time one is over

1. Get the path of the photo for the prayer time card
2. render the card with the information passed in from the Parameters
*/

class PrayerTime extends Component {

    constructor(props) {
        super(props)
    
        this.picsize = "70px"; //Size of the image for this prayer card
    }

    /**
     * The function `getPhotoPath` takes a prayer name as input and returns the corresponding photo
     * path based on the prayer type.
     * @param prayer - The `getPhotoPath` function takes a parameter `prayer` which represents
     * different prayer times such as Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha. The function
     * returns the corresponding picture path based on the input prayer time.
     * @returns The function `getPhotoPath(prayer)` returns the photo path based on the input `prayer`.
     * The specific photo path returned depends on the value of the `prayer` parameter.
     */
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
                    <label>{this.props.start}</label>
                </div>
                <div>
                    <label>{this.props.prayer}</label>
                </div>
                <img    src={this.getPhotoPath(this.props.prayer)} 
                            alt={this.props.prayer}
                            style={{ width: this.picsize, height: this.picsize, objectFit: 'cover' }}
                    ></img>
                <div>
                    <label style={{fontSize: '40px' }}>{this.props.iqamah}</label>
                </div>
            </div>
        )
    }
}

export default PrayerTime