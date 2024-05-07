import React, { Component } from 'react'

/*
Displays the countdown until next Salah

Parameters passed from Parent
- salah: The next Salah that is being counted down to
- type:     time: the 'finish_time' passed in is for actual start of the time for prayer (Usually comes before the iqamah)
            iqamah: the 'finish_time' passed in is for the iqamah
            khutbah: the 'finish_time' passed in is for the jummah khutbah time
- finish_time: The time that the countdown will end at
- callback: function located in the Parent Component to fetch the next prayer time after time one is over

1. Initialize Contructor
2. componentDidMount is called
    a. Get the remaining number of seconds until the countdown finishes
    b. Convert it into HH:MM:SS value for remaining hours, minutes, and seconds
3. componentDidUpdate is called
    a. Set the message to be displayed above the Countdown (Ex: "Duhr is in")
    b. Begin the Timer
4. Render Countdown and update every second
*/

class Countdown extends React.Component {
    constructor(props) {
        console.log('constructor: ');
        super(props);
        this.state = {  
            UI_time: {},
            salah: this.props.salah,
            message: ""
            };
        this.finish_time = this.props.finish_time
        this.timer = 0;
        this.countDown = this.countDown.bind(this);
        this.callback = this.props.callback.bind();
        this.start=false;
    }

    /**
     * The function `get_UI_time` converts a given number of seconds into hours, minutes, and seconds and
     * returns an object with these values.
     * @param secs - The `secs` parameter in the `get_UI_time` function represents the total number of
     * seconds that you want to convert into hours, minutes, and seconds.
     * @returns An object containing the hours, minutes, and seconds calculated from the input number of
     * seconds is being returned.
     */
    get_UI_time(secs){
        let hours = Math.floor(secs / (60 * 60));

        let divisor_for_minutes = secs % (60 * 60);
        let minutes = Math.floor(divisor_for_minutes / 60);

        let divisor_for_seconds = divisor_for_minutes % 60;
        let seconds = Math.ceil(divisor_for_seconds);

        let obj = {
            "h": hours,
            "m": minutes,
            "s": seconds
        };
        return obj;
    }

    componentDidUpdate(prevProps, prevState, snapshot){
        if(!this.start && this.props.finish_time !== this.finish_time ){            
            console.log("starting countdown")
            
            //Customize the message above the countdown. Yes this part is a bit hacky and I prob could've done it better but it works
            var Message = "";
            if (this.props.salah === "Sunrise") {
                Message = "Sunrise is in"
            }
            else if (this.props.type === "time") {
                Message = this.props.salah + " is in"
            }
            else if (this.props.type === "iqamah") {
                Message = this.props.salah + " Iqamah is in"
            }
            else if (this.props.salah === "Jummah" && this.props.type === "khutbah") {   //For Jummah only
                Message = this.props.salah + " Khutbah is in"
            }

            //update the countdown message
            this.setState({
                salah: this.props.salah,
                message: Message, 
            })

            //This is done once at the start of each countdown
            this.finish_time = new Date(Date.parse(this.props.finish_time))     //When the countdown should end
            this.timer = setInterval(this.countDown, 1000);                     //How often the countdown should be updates in milliseconds
            this.start = true;                                                  //Flag signalling countdown has been set to prevent running this method more times than required and causing wierd bugs
            this.callback = this.props.callback.bind(this)                      //When the countdown hits the finish time, it calls back to the Main.js nextPrayerCountdown() method to get the next countdown
        }
    }

    componentDidMount(){
        var seconds = (this.state.finish_time - (new Date()) / 1000)+1  //Get the difference in time between the time right now and the finish time. Convert it into seconds remaining
        var timeLeftVar = this.get_UI_time(seconds);                    //Convert reminaing seconds into remaining hours, minutes, and seconds format to be displayed
        //display remaining time
        this.setState({ 
            UI_time: timeLeftVar 
        });
    }

    /**
     * The `countDown` function in JavaScript updates the UI time every second and triggers a callback
     * when the countdown reaches zero. The callback is the nextPrayerCountdown() method in Main.js to retrieve the next countdown
     */
    countDown() {
      // Remove one second, set state so a re-render happens.
        let seconds = parseInt((this.finish_time - (new Date())) / 1000)+1;
        this.setState({
            UI_time: this.get_UI_time(seconds),
        });
        
        // Check if we're at zero. If we hit zero, go to callback functions and retrieve the enxt countdown
        if (seconds <= 0) { 
            clearInterval(this.timer);
            setTimeout(null,2000);
            this.start = false
            this.callback();
            console.log('callback to get countdown for next prayer: ');
        }
    }

    render() {
        return(
            <div>
                {this.state.message} <br></br> {('0' + this.state.UI_time.h).slice(-2)} : {('0' + this.state.UI_time.m).slice(-2)} : {('0' + this.state.UI_time.s).slice(-2)}
            </div>
        );
    }
}

export default Countdown