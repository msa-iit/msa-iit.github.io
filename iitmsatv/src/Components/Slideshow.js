import React, { Component, useRef } from 'react';
import './Style.css'; // Import the CSS file for styling

class Slideshow extends Component {
    constructor(props) {
        super(props);

        // Initialize state
        this.state = {
            currentImageIndex: 0,
            imageList: [],
            fading: false,
            // scalingPercentage: 80, // Initial scaling percentage (adjust as needed)
        };
        this.slideshow_delay = 10;
        this.maxwidth = "1000px"
        this.maxheight = "720px"
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
        Promise.all([fetch("http://localhost:7000/slideshowDelay").then(res => res.text())])
        .then(([slideshowDelay]) => {
            this.slideshow_delay = parseInt(slideshowDelay);
            this.loadImageList();
            this.slideshowInterval = setInterval(this.nextImage, this.slideshow_delay * 1000);
        })
    };

    // Function to load the image list from the folder
    loadImageList = () => {
        const imageContext = require.context('../images/Slideshow', false, /\.(jpg|jpeg|png|gif)$/);
        const imageList = imageContext.keys().map(imageContext);
        this.setState({ imageList });
    };

    nextImage = () => {
        // Get the next image index
        const { currentImageIndex, imageList } = this.state;
        const nextIndex = (currentImageIndex + 1) % imageList.length;

        // Check if it's the last image and reload the image list
        if (nextIndex === 0) {
            this.loadImageList();
        }

        // Update the state to trigger the fading animation
        this.setState({
            fading: true,
        });

        // After a brief delay, update the state to display the next image and reset the fading animation
        setTimeout(() => {
            this.setState({
                currentImageIndex: nextIndex,
                fading: false,
            });
        }, 500);
    };

    // // Function to handle scaling percentage change
    // handleScalingChange = (event) => {
    //     const scalingPercentage = parseInt(event.target.value);
    //     this.setState({ scalingPercentage });
    // };

    // // Function to handle image load
    // handleImageLoad = (event) => {
    //     const image = event.target;
    //     const scalingPercentage = this.calculateScalingPercentage(image);
    //     this.setState({ scalingPercentage });
    // };

    // // Function to calculate the scaling percentage based on image height
    // calculateScalingPercentage = (image) => {
    //     const maxHeight = 720;
    //     const originalHeight = image.clientHeight;
    //     if (originalHeight <= maxHeight) {
    //         return 100; // No scaling required
    //     } else {
    //         return (maxHeight / originalHeight) * 100;
    //     }
    // };

    ImageBoundaries(image) {
        console.log('image: ', image)
        if (image.current === null) {
            return [this.maxheight, "auto"]
        }
        const { naturalWidth, naturalHeight } = image.current;
        var width = naturalWidth
        console.log('width: ', width)
        var height = naturalHeight
        console.log('height: ', height)

        if (height < width) {
            return ["auto", this.maxwidth]
        }
        else {
            return [this.maxheight, "auto"]
        }
    }

    render() {
        const { currentImageIndex, imageList, fading } = this.state;
        const currentImage = imageList[currentImageIndex];
        var dimensions = this.ImageBoundaries(React.createRef(currentImage));
        console.log('dimensions[0]: ', dimensions[0])
        console.log('dimensions[1]: ', dimensions[1])

        // Apply the fading animation class conditionally
        const imageClassName = `slider-image ${fading ? 'fade' : ''}`;

        return (
            <div className={imageClassName} style={{ alignItems: 'center' }}>
                <img
                    src={currentImage}
                    alt={`${currentImageIndex + 1}`}
                    onLoad={this.handleImageLoad}
                    style={{
                        height: dimensions[0],
                        width: dimensions[1],
                    }}
                />
            </div>
        );
    }
}

export default Slideshow;
