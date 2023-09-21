import React, { useState, useEffect } from 'react';
import Ticker from 'react-ticker'

const GetAnnouncements = () => {
    const [announcements, setAnnouncements] = useState([]);
    useEffect(() => {
        Promise.resolve(fetch("http://localhost:7000/Announcements"))
        .then(res => res.text())
        .then((result) => {
            setAnnouncements(result.slice(1,-2).replace(/"/g, '').trim().split(','));
        })
        }, []);
        // A placeholder is needed, to tell react-ticker, that width and height might have changed
        // It uses MutationObserver internally
        return (announcements && isNaN(announcements[0])) ? (
            <p>{announcements.join(" ------ ")} /</p>
        ) : (
            <p style={{ visibility: "hidden" }}>No Announcements</p>
        );
    };
    
function AnnouncementTicker() {
    return (
    <Ticker offset="run-in" speed={5} mode="await">
        {() => <GetAnnouncements />}
    </Ticker>
    );
}

export default AnnouncementTicker;