import React, { useState, useEffect } from 'react';
import Ticker from 'react-ticker'

const GetAnnouncements = () => {
    const [announcements, setAnnouncements] = useState([]);
    useEffect(() => {
        Promise.resolve(fetch("http://localhost:7000/Announcements"))
        .then(res => res.text())
        .then((result) => {
            setAnnouncements(result.slice(1,-1).replace(/"/g, '').split(','));
        })
        }, []);
        // A placeholder is needed, to tell react-ticker, that width and height might have changed
        // It uses MutationObserver internally
        return announcements ? (
            <p>{announcements.join(" +++ ")} / </p>
        ) : (
            <p style={{ visibility: "hidden" }}>No Announcements</p>
        );
    };
    
function StockTicker() {
    return (
    <Ticker offset="run-in" speed={5} mode="await">
        {() => <GetAnnouncements />}
    </Ticker>
    );
}

export default StockTicker;