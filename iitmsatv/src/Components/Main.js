import React, { Component } from 'react'
import PrayerTime from './PrayerTime'
import ListGroup from 'react-bootstrap/ListGroup';
import Countdown from './Countdown';
import Slideshow from './Slideshow'
import msa_logo from "../images/msa_logo.png"
import './Style.css'
import Clock from './Clock';

class Main extends Component {

    constructor(props) {
        super(props)

        this.Today_Prayer_Times = {};   // JSON that holds information about today's prayer times retrieved from Flask
        this.Iqamah_Times = {};         // JSON that holds information about iqamah times retrieved from Flask
        this.setTimes = true;           // Boolean used to only set the React State once and populate data on startup
        this.logosize = '200px';        // Size of the MSA logo at the top right of the display
        this.state = {
            Gregorian_Date: "",         //Todays Date (Gregorian format)
            Hijri_Date: "",             //Todays Date (Hijri format)
            Fajr: {                     //Fajr Prayer info
                start: "",
                iqamah: "",
                next: false
            },
            Sunrise: {                  //Sunrise Prayer info
                start: "",
                next: false
            },
            Dhuhr: {                    //Dhuhr Prayer info
                start: "",
                iqamah: "",
                next: false
            },
            Asr:  {                     //Asr Prayer info
                start: "",
                iqamah: "",
                next: false
            },
            Maghrib: {                  //Maghrib Prayer info
                start: "",
                iqamah: "",
                next: false
            },
            Isha: {                     //Isha Prayer info
                start: "",
                iqamah: "",
                next: false
            },
            Jummah: {                   //Jummah Prayer info
                start: "",
                iqamah: "",
                next: false
            },
            Next_Salah: {               //Which Prayer is next and its info
                prayer: null,
                type: null,
                time: null
            }
        }
    }

    /**
     * Native React Function
     * Called after render() is called
     */
    componentDidMount() {
        console.log('componentDidMount');
        // Add data once
        if(this.setTimes){
            this.setPrayerTimeData();
        }
    }

    /**
     * Callback function for Countdown Component
     * Keep it in the "function = () => {}" format in order for the callback functionality to work 
     */
    nextPrayerCountdown = () => {
        this.setPrayerTimeData();
    }

    /**
     * Set the State with new prayer time data
    */
    setPrayerTimeData(){
        //Fetch data from Flask API
        Promise.all([fetch("http://localhost:7000/Iqamahs").then(res => res.json()),            // Iqamahs
                    fetch("http://localhost:7000/prayerTimesToday").then(res => res.json()),    // prayer times for today
                    fetch("http://localhost:7000/todayHijri").then(res => res.text()),          // hijri date
                    fetch("http://localhost:7000/NextSalah").then(res => res.json()),           // info about next salah for countdown
                    fetch("http://localhost:7000/todayGreg").then(res => res.text())])          // regular date
        .then(([iqamah_times, today_times, hijri_date, nextSalah, greg_date]) => {
            this.Today_Prayer_Times = today_times;
            this.Iqamah_Times = iqamah_times;
            this.start = true;
            //Populating this.State automatically updates the display
            this.setState(({
                Gregorian_Date: greg_date,
                Hijri_Date: hijri_date,
                Fajr: {
                    start: today_times.Fajr,
                    iqamah: iqamah_times.Fajr,
                    next: nextSalah.prayer === "Fajr"
                },
                Sunrise: {  //I just labeled Sunrise as a prayer just so the countdown and Sunrise time component would work simply. It does not have an Iqamah property tho
                    start: today_times.Sunrise,
                    next: nextSalah.prayer === "Sunrise"
                },
                Dhuhr: {
                    start: today_times.Dhuhr,
                    iqamah: iqamah_times.Dhuhr,
                    next: nextSalah.prayer === "Dhuhr"
                },
                Asr: {
                    start: today_times.Asr,
                    iqamah: iqamah_times.Asr,
                    next: nextSalah.prayer === "Asr"
                },
                Maghrib: {
                    start: today_times.Maghrib,
                    iqamah: iqamah_times.Maghrib,
                    next: nextSalah.prayer === "Maghrib"
                },
                Isha: {
                    start: today_times.Isha,
                    iqamah: iqamah_times.Isha,
                    next: nextSalah.prayer === "Isha"
                },
                Jummah: {
                    start: iqamah_times["Jummah Khutbah"],
                    iqamah: iqamah_times["Jummah Iqamah"],
                    next: nextSalah.prayer === "Jummah"
                },
                Next_Salah: {
                    prayer: nextSalah.prayer,
                    type: nextSalah.type,
                    time: nextSalah.time
                }
            }))
            console.log("MAIN: State is set");
            this.setTimes = false;
        })

        
    }

    render() {
        console.log('rendered');
        return (
            <body>
                
                <div id='fullContainer'>
                    <div id="leftContainer">
                        <div id='slideshow'>
                            <Slideshow></Slideshow>
                        </div>
                        <div id='PrayerCardsList'>
                            <ListGroup horizontal>
                                <ListGroup.Item active={this.state.Next_Salah.prayer === "Sunrise"}>
                                    <PrayerTime prayer='Fajr' 
                                                start={this.state.Fajr.start} 
                                                iqamah={this.state.Fajr.iqamah} 
                                                selected={this.state.Fajr.selected}></PrayerTime>
                                </ListGroup.Item>

                                <ListGroup.Item active={this.state.Next_Salah.prayer === "Dhuhr" || this.state.Next_Salah.prayer === "Jummah"}>
                                    <PrayerTime prayer='Sunrise' 
                                                start={this.state.Sunrise.start} 
                                                iqamah={""} 
                                                selected={this.state.Sunrise.selected}></PrayerTime>
                                </ListGroup.Item>

                                <ListGroup.Item active={this.state.Next_Salah.prayer === "Asr"}>
                                    <PrayerTime prayer='Dhuhr' 
                                                start={this.state.Dhuhr.start} 
                                                iqamah={this.state.Dhuhr.iqamah} 
                                                selected={this.state.Dhuhr.selected}></PrayerTime>
                                </ListGroup.Item>

                                <ListGroup.Item active={this.state.Next_Salah.prayer === "Maghrib"}>
                                    <PrayerTime prayer='Asr' 
                                                start={this.state.Asr.start} 
                                                iqamah={this.state.Asr.iqamah} 
                                                selected={this.state.Asr.selected}></PrayerTime>
                                </ListGroup.Item>

                                <ListGroup.Item active={this.state.Next_Salah.prayer === "Isha"}>
                                    <PrayerTime prayer='Maghrib' 
                                                start={this.state.Maghrib.start} 
                                                iqamah={this.state.Maghrib.iqamah} 
                                                selected={this.state.Maghrib.selected}></PrayerTime>
                                </ListGroup.Item>

                                <ListGroup.Item active={this.state.Next_Salah.prayer === "Fajr"}>
                                    <PrayerTime prayer='Isha' 
                                                start={this.state.Isha.start} 
                                                iqamah={this.state.Isha.iqamah} 
                                                selected={this.state.Isha.selected}></PrayerTime>
                                </ListGroup.Item>
                            </ListGroup>
                        </div>
                    </div>
                    <div id='rightContainer'>
                        <div id="sideinfo">
                                <h1 id='TitleDisplay'>Welcome to IIT MSA</h1>
                                <div    id='Logo'>
                                    <img    src={msa_logo} 
                                            alt="iit msa logo"
                                            style={{ width: this.logosize, height: this.logosize, objectFit: 'cover' }}
                                    ></img>
                                </div>
                                <div id='Clock'>
                                    <Clock></Clock>
                                </div>
                                <hr className="centered-hr"></hr>
                                <label id='CountdownDisplay'>
                                    <Countdown  salah={this.state.Next_Salah.prayer}
                                                type={this.state.Next_Salah.type}
                                                finish_time={this.state.Next_Salah.time} 
                                                callback={this.nextPrayerCountdown}></Countdown>
                                </label>
                                <hr className="centered-hr"></hr>
                                <div id='DatesContainer'>
                                    <div>
                                        <label id='DateDisplay'>{this.state.Hijri_Date}</label>
                                    </div>
                                    <div>
                                        <label id='DateDisplay'>{this.state.Gregorian_Date}</label>
                                    </div>
                                </div>
                                <h2 id='JummahDisplay'>
                                    Jummah Khutbah <br></br> {this.state.Jummah.start}
                                </h2>
                                <h2 id='JummahDisplay'>
                                    Jummah Salah <br></br> {this.state.Jummah.iqamah}
                                </h2>
                        </div>
                    </div>
                    <div>
                        <label id="suggestLabel">This is a work in progress. Send suggestions to msa@iit.edu</label>
                    </div>
                </div>
            </body>
        )
    }
}

export default Main