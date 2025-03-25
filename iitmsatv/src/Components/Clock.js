import React, { Component } from 'react';

/*
Controls the clock of the display to show the current hour and minute
1. Get the current hour and minute
2. Parse the values so they are in HH:MM format and 12-Hour AM/PM format
3. Repeat steps 1-2 every second
*/

class Clock extends Component {
    constructor(props) {
        super(props);
        this.state = {
        currentTime: this.getCurrentTime(),
        };
    }

    componentDidMount() {
        // Set up an interval to update after a certain number of milliseconds
        this.intervalId = setInterval(() => {
            this.setState({
                currentTime: this.getCurrentTime(),
            });
        }, 1000); // 60000 milliseconds = 1 minute
    }

    componentWillUnmount() {
        // Clear the interval when the component is unmounted
        clearInterval(this.intervalId);
    }

    /**
     * The function getCurrentTime returns the current time in a formatted 12-hour clock format with AM
     * or PM.
     * @returns The `getCurrentTime()` function returns the current time in 12-hour format with AM or
     * PM.
     */
    getCurrentTime() {
        const now = new Date();
        const hours = now.getHours();
        const minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        const formattedHours = hours % 12 === 0 ? 12 : hours % 12;
        const formattedMinutes = minutes < 10 ? `0${minutes}` : minutes;
        return `${formattedHours}:${formattedMinutes} ${ampm}`;
    }

    render() {
        return (
        <div>
            <label>{this.state.currentTime}</label>
        </div>
        );
    }
}

export default Clock;
