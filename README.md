# Image Stitcher App

This Streamlit app allows users to upload multiple images, adjust their order, choose padding or scaling for shorter images, and stitch them together into one composite image. Users can also adjust the final dimensions of the stitched image using a slider and download the resulting image.

## Features

- **Drag and Drop Upload**: Easily upload multiple images by dragging and dropping them into the app.
- **Reorder Images**: Change the order of uploaded images using a text input to specify the desired order.
- **Padding or Scaling**: Choose whether to pad shorter images with a white rectangle or scale them to match the height of the tallest image.
- **Add Border**: Add a white border around each image and specify the width in pixels.
- **Adjust Dimensions**: Use a slider to scale the final composite image by a percentage, dynamically displaying the final width and height.
- **Resolution Settings**: Select whether the final image resolution is (a) original resolution, (b) optimised for screen (72 dpi), or (c) optimised for print (300 dpi).
- **Filename Validation**: Enter a custom filename for the stitched image, validated for special characters and correct extension.
- **Download Stitched Image**: Download the stitched image in JPEG format.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/gauden/image-stitcher-app.git
    cd image-stitcher-app
    ```

2. **Create and Activate a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Libraries**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the App**:
    ```bash
    streamlit run app.py
    ```

2. **Open the App in Your Browser**:
    Follow the URL provided by Streamlit (usually `http://localhost:8501`).

3. **Upload and Stitch Images**:
    - Upload images by dragging and dropping them into the app.
    - Reorder images by entering the desired order in the text input field.
    - Select padding or scaling options for shorter images.
    - Add a white border and specify the width in pixels.
    - Adjust the final image dimensions using the slider.
    - Select the desired resolution for the final image.
    - Enter a custom filename for the stitched image.
    - Click "Stitch Images" to see the result and download the stitched image.

## Requirements

The required Python libraries are listed in the `requirements.txt` file:

- streamlit
- pillow

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Pillow (PIL Fork)](https://python-pillow.org/)
