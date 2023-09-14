import React, { Component } from 'react';
import './Style.css'; // Import the CSS file for styling

class Slideshow extends Component {
    constructor(props) {
        super(props);

        // Use require.context to dynamically import images from the directory
        const imageContext = require.context('../images/Slideshow', false, /\.(jpg|jpeg|png|gif)$/);
        const imageList = imageContext.keys().map(imageContext);

        // Initialize state
        this.state = {
        currentImageIndex: 0,
        imageList,
        fading: false,
        };
        this.picsize = '600px'
    }

    componentDidMount() {
        // Start the slideshow when the component mounts
        this.startSlideshow();
    }

    componentWillUnmount() {
        // Clear the interval when the component unmounts to prevent memory leaks
        clearInterval(this.slideshowInterval);
    }

    startSlideshow = () => {
        // Set an interval to switch images every 10 seconds
        this.slideshowInterval = setInterval(this.nextImage, 5000);
    };

    nextImage = () => {
        // Get the next image index
        const { currentImageIndex, imageList } = this.state;
        const nextIndex = (currentImageIndex + 1) % imageList.length;

        // Update the state to trigger the fading animation
        this.setState({
        fading: true,
        });

        // After a brief delay (500ms), update the state to display the next image and reset the fading animation
        setTimeout(() => {
        this.setState({
            currentImageIndex: nextIndex,
            fading: false,
        });
        }, 500);
    };

    render() {
        const { currentImageIndex, imageList, fading } = this.state;
        const currentImage = imageList[currentImageIndex];

        // Apply the fading animation class conditionally
        const imageClassName = `slider-image ${fading ? 'fade' : ''}`;

        return (
            <div    className={imageClassName}
                    style={{alignItems:'center'}}>
                <img
                    src={currentImage}
                    alt={`${currentImageIndex + 1}`}
                    style={{ width: this.picsize, height: this.picsize}} // Set your desired width and height here
                />
            </div>
        );
    }
}

export default Slideshow;
