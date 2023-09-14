import React, { Component } from 'react'
import PrayerTime from './PrayerTime'
import ListGroup from 'react-bootstrap/ListGroup';
import Countdown from './Countdown';
import Announcements from "./Announcements"
import Slideshow from './Slideshow'
import msa_logo from "../images/msa_logo.png"
import './Style.css'
import Clock from './Clock';

class Main extends Component {

    constructor(props) {
        super(props)

        this.Today_Prayer_Times = {};
        this.Iqamah_Times = {};
        this.setTimes = true;
        this.logosize = '30%';
        this.state = {
            Gregorian_Date: "",
            Hijri_Date: "",
            Fajr: {
                start: "",
                iqamah: "",
                selected: false
            },
            Sunrise: {
                start: "",
                selected: false
            },
            Dhuhr: {
                start: "",
                iqamah: "",
                selected: false
            },
            Asr:  {
                start: "",
                iqamah: "",
                selected: false
            },
            Maghrib: {
                start: "",
                iqamah: "",
                selected: false
            },
            Isha: {
                start: "",
                iqamah: "",
                selected: false
            },
            Jummah: {
                start: "",
                selected: false
            },
            next_salah_time: null,
            next_salah:""
        }
    }

    /**
     * Native React Function
     * Called after render() is called
     */
    componentDidMount() {
        console.log('componentDidMount');
        if(this.setTimes){
            this.setPrayerTimeData();
        }
    }

    /**
     * Callback function for Countdown Component
     * Keep it in the "function = () => {}" formal in order for the callback functionality to work 
     */
    nextPrayerCountdown = () => {
        console.log('nextPrayerCountdown: ');
        this.setPrayerTimeData();
    }

    /**
     * Set the State with new prayer time data
     */
    setPrayerTimeData(){
        Promise.all([fetch("http://localhost:7000/Iqamahs").then(res => res.json()),
                    fetch("http://localhost:7000/prayerTimesToday").then(res => res.json()),
                    fetch("http://localhost:7000/todayHijri").then(res => res.text()),
                    fetch("http://localhost:7000/NextSalah").then(res => res.json()),
                    fetch("http://localhost:7000/todayGreg").then(res => res.text())])
        .then(([iqamah_times, today_times, hijri_date, nextSalah, greg_date]) => {
            // console.log('nextSalah: ', nextSalah);
            this.Today_Prayer_Times = today_times;
            this.Iqamah_Times = iqamah_times;
            this.start = true;
            // console.log("this.state.next_salah_time", this.state.next_salah_time)
            // console.log('nextSalah.time: ', nextSalah.time);
            this.setState(({
                Gregorian_Date: greg_date,
                Hijri_Date: hijri_date,
                Fajr: {
                    start: today_times.Fajr,
                    iqamah: iqamah_times.Fajr,
                    selected: nextSalah.prayer === "Fajr"

                },
                Sunrise: {  //Yeah I just labeled Sunrise as a prayer just so the countdown and Sunrise time component would work simply. It does not have an Iqamah property tho
                    start: today_times.Sunrise,
                    selected: nextSalah.prayer === "Sunrise"
                },
                Dhuhr: {
                    start: today_times.Dhuhr,
                    iqamah: iqamah_times.Dhuhr,
                    selected: nextSalah.prayer === "Dhuhr"
                },
                Asr: {
                    start: today_times.Asr,
                    iqamah: iqamah_times.Asr,
                    selected: nextSalah.prayer === "Asr"
                },
                Maghrib: {
                    start: today_times.Maghrib,
                    iqamah: iqamah_times.Maghrib,
                    selected: nextSalah.prayer === "Maghrib"
                },
                Isha: {
                    start: today_times.Isha,
                    iqamah: iqamah_times.Isha,
                    selected: nextSalah.prayer === "Isha"
                },
                Jummah: {
                    start: iqamah_times.Jummah,
                    selected: nextSalah.prayer === "Jummah"
                },
                next_salah_time: nextSalah.time,
                next_salah: nextSalah.salah
            }))
            console.log("MAIN: State is set");
            this.setTimes = false;
        })

        
    }

    /**
     * Takes a string in the format "hh:mm (CDT)" and converts it into hh:mm (am/pm)
     * Ex: 18:10 (CDT) --> 6:10 pm 
     * @param {string} time 
     * @returns {string}
     */
    formatTime(time){
        var newTime = `${time}`;    //Quick way to create full copy of 'time'. Can't use var newTime = time; Because that causes newtime -> time which would modify 'time' directly. We don't want that we want a full copy of 'time'
        newTime = newTime.replace('(CDT)','');

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
        else{
            newTime = newTime + ' AM';
        }
        // console.log("new time: " + newTime);
        return newTime;
    }

    render() {
        // console.log('rendered');
        return (
            <div id='fullContainer'>
                <div id="leftContainer">
                    <div id='slideshow'>
                        <Slideshow></Slideshow>
                    </div>
                    <div id='PrayerCardsList'>
                        <ListGroup horizontal>
                            <ListGroup.Item variant="secondary">
                                <PrayerTime type='Fajr' start={this.state.Fajr.start} iqamah={this.state.Fajr.iqamah} selected={this.state.Fajr.selected}></PrayerTime>
                            </ListGroup.Item>

                            <ListGroup.Item variant="secondary">
                                <PrayerTime type='Sunrise' start={this.state.Sunrise.start} iqamah={""} selected={this.state.Sunrise.selected}></PrayerTime>
                            </ListGroup.Item>

                            <ListGroup.Item variant="secondary">
                                <PrayerTime type='Dhuhr' start={this.state.Dhuhr.start} iqamah={this.state.Dhuhr.iqamah} selected={this.state.Dhuhr.selected}></PrayerTime>
                            </ListGroup.Item>

                            <ListGroup.Item variant="secondary">
                                <PrayerTime type='Asr' start={this.state.Asr.start} iqamah={this.state.Asr.iqamah} selected={this.state.Asr.selected}></PrayerTime>
                            </ListGroup.Item>

                            <ListGroup.Item variant="secondary">
                                <PrayerTime type='Maghrib' start={this.state.Maghrib.start} iqamah={this.state.Maghrib.iqamah} selected={this.state.Maghrib.selected}></PrayerTime>
                            </ListGroup.Item>

                            <ListGroup.Item variant="secondary">
                                <PrayerTime type='Isha' start={this.state.Isha.start} iqamah={this.state.Isha.iqamah} selected={this.state.Isha.selected}></PrayerTime>
                            </ListGroup.Item>

                            {/* <ListGroup.Item>
                                <PrayerTime type='Jummah' start={this.state.Jummah.start} iqamah="" selected={this.state.Jummah.selected}></PrayerTime>
                            </ListGroup.Item> */}
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
                            <h3 id='DateDisplay'>{this.state.Hijri_Date}</h3>
                            <h3 id='DateDisplay'>{this.state.Gregorian_Date}</h3>
                            <h2 id='CountdownDisplay'>
                                <Countdown salah={this.state.next_salah} finish_time={this.state.next_salah_time} callback={this.nextPrayerCountdown}></Countdown>
                            </h2>
                            <h2 id='DateDisplay'>
                                Jummah <br></br> {this.formatTime(this.state.Jummah.start)}
                            </h2>
                    </div>
                </div>
                <div id="Announcements">
                    <Announcements></Announcements>
                </div>
            </div>
        )
    }
}

export default Main