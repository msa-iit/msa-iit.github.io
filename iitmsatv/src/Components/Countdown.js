import React, { Component } from 'react'


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
        console.log('componentDidUpdate: this.finish_time: ', this.finish_time);
        console.log('componentDidUpdate: this.props.finish_time: ', this.props.finish_time);
        console.log('this.start: ', this.start);
        if(!this.start && this.props.finish_time !== this.finish_time ){            
            console.log("starting countdown")
            var Message = "";
            if(this.props.salah === "End of Day"){
                Message = "End of Day is in"
            }
            else{
                Message = this.props.salah + " Salah is in"
            }
            this.setState({
                salah: this.props.salah,
                message: Message, 
            })
            this.finish_time = new Date(Date.parse(this.props.finish_time))
            this.timer = setInterval(this.countDown, 1000);
            this.start = true;
            this.callback = this.props.callback.bind(this)
        }
    }

    componentDidMount(){
        // console.log('componentDidMount: this.state.finish_time: ', this.state.finish_time);
        var seconds = (this.state.finish_time - (new Date()) / 1000)+1
        var timeLeftVar = this.get_UI_time(seconds);
        this.setState({ 
            UI_time: timeLeftVar 
        });
    }

    countDown() {
      // Remove one second, set state so a re-render happens.
        let seconds = parseInt((this.finish_time - (new Date())) / 1000)+1;
        this.setState({
            UI_time: this.get_UI_time(seconds),
        });
        
        // Check if we're at zero.
        if (seconds <= 0) { 
            clearInterval(this.timer);
            setTimeout(null,2000);
            this.start = false
            console.log('start changed to false');
            this.callback();
            console.log('callback: ');
        }
    }

    render() {
        // console.log('Countdown: rendered');
        // console.log('this.state.UI_time.h: ', this.state.UI_time.h);
        // console.log('this.state.UI_time.m: ', this.state.UI_time.m);
        // console.log('this.state.UI_time.s: ', this.state.UI_time.s);
        return(
            <div>
                {this.state.message} <br></br> {('0' + this.state.UI_time.h).slice(-2)}h {('0' + this.state.UI_time.m).slice(-2)}m {('0' + this.state.UI_time.s).slice(-2)}s
            </div>
        );
    }
}

export default Countdown


// import React from 'react'

// function Countdown() {
//     return (
//     <div>Countdown</div>
//     )
// }

// export default Countdown