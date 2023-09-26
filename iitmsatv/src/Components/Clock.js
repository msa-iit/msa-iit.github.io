import React, { Component } from 'react';

class Clock extends Component {
    constructor(props) {
        super(props);
        this.state = {
        currentTime: this.getCurrentTime(),
        };
    }

    componentDidMount() {
        // Set up an interval to update the time every minute
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
