import React, { Component } from 'react';
import './Style.css'; // Import the CSS file for styling
import NoImageDefault from "../images/msa_logo.png"

/*
Displays images from the MSA Dropbox under MSA_TV/Slideshow Pictures

1. Initialize Constructor
2. ComponentDidMount
    a. Query the API to retrieve the slideshow delay (How long each image should be displayed for before switching to the next image)
    b. Query the API to retrieve a list of urls for each of the images hosted on the dropbox
3. Begin the slideshow and set the timer to switch through each image
4. When rendering each image, calculate boundaries so the image does not exceed the image box area
*/

class Slideshow extends Component {
    constructor(props) {
        super(props);

        // Initialize state
        this.state = {
            currentImageIndex: 0,
            imageList: [],
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

    /* The `startSlideshow` function is making a request to the Flask API to fetch the slideshow delay time. Once the response is
    received, it parses the delay time to an integer and sets it to the global variable `this.slideshow_delay`. 
    */
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
            if(imageList.length === 0){
                imageList = [NoImageDefault]
            }
            this.setState({ imageList });
        })

        //This was the old implementation where we used to manually upload the slideshow photos onto the masjid laptop. This is deprecated since we can now use Dropbox
        // const imageContext = require.context('../images/Slideshow', false, /\.(jpg|jpeg|png|gif)$/);
        // var imageList = imageContext.keys().map(imageContext);
        // console.log('imageList: ', imageList)
        // this.setState({ imageList });
    };

    /* The `nextImage` function in the provided code is responsible for transitioning to the next image in
    the slideshow. 
    */
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

    /**
     * The function `ImageBoundaries` determines the appropriate width and height values for an image
     * based on its natural dimensions.
     * @param image - The `image` parameter in the `ImageBoundaries` function is expected to be a
     * reference to an image element in the DOM. It seems like the function is checking the dimensions
     * of the image to determine its boundaries based on whether the height is less than the width. The
     * function returns an array with
     * @returns The ImageBoundaries function returns an array with two values. The first value is
     * either "auto" or the maximum height value, and the second value is either "auto" or the maximum
     * width value, depending on the dimensions of the image.
     */
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
        const { currentImageIndex, imageList } = this.state;
        const currentImage = imageList[currentImageIndex];                      //Current image of the slideshow
        var dimensions = this.ImageBoundaries(React.createRef(currentImage));   //dimensions of the image

        return (
            <div style={{ alignItems: 'center' }}>
                <img
                    src={currentImage}
                    alt={"Slideshow Loading..."}
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
