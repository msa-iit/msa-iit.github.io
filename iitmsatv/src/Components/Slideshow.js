import React, { Component } from 'react';
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
        this.slideshow_delay = 15;
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
        Promise.all([fetch("http://localhost:7000/SlideshowDelay").then(res => res.text())])
        .then(([slideshowDelay]) => {
            this.slideshow_delay = parseInt(slideshowDelay);
            this.loadImageList();
            this.slideshowInterval = setInterval(this.nextImage, this.slideshow_delay * 1000);
        })

    };

    // Function to load the image list from the folder
    loadImageList = () => {
        Promise.resolve(fetch("http://localhost:7000/LoadImages").then(res => res.json())).then((imageList) =>{
            console.log(imageList)
            // this.setState({ imageList });
        })
        const imageContext = require.context('../images/Slideshow', false, /\.(jpg|jpeg|png|gif)$/);
        const imageList = imageContext.keys().map(imageContext);
        console.log('imageList: ', imageList)
        this.setState({ imageList });
    };

    nextImage = () => {
        // Get the next image index
        const { currentImageIndex, imageList } = this.state;
        const nextIndex = (currentImageIndex + 1) % imageList.length;
        console.log('nextIndex: ', nextIndex)

        // Check if it's the last image then reload the image list
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

    ImageBoundaries(image) {
        if (image.current === null) {
            return [this.maxheight, "auto"]
        }
        const { naturalWidth, naturalHeight } = image.current;
        var width = naturalWidth
        var height = naturalHeight

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
        // console.log('dimensions[0]: ', dimensions[0])
        // console.log('dimensions[1]: ', dimensions[1])

        // Apply the fading animation class conditionally
        const imageClassName = `slider-image ${fading ? 'fade' : ''}`;

        return (
            <div className={imageClassName} style={{ alignItems: 'center' }}>
                <img
                    src={currentImage}
                    referrerPolicy="no-referrer"
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
