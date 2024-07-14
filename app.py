import streamlit as st
from PIL import Image, ImageOps
import io
import re


def stitch_images(images, pad_or_scale, scale_percentage, border_width, resolution):
    widths, heights = zip(*(i.size for i in images))

    # Add border to images
    if border_width > 0:
        images = [
            ImageOps.expand(image, border=border_width, fill="white")
            for image in images
        ]
        widths, heights = zip(*(i.size for i in images))

    if pad_or_scale == "Scale":
        max_height = max(heights)
        images = [
            ImageOps.fit(
                image,
                (image.width, max_height),
                method=Image.Resampling.LANCZOS,
                bleed=0.0,
                centering=(0.5, 0.5),
            )
            for image in images
        ]
    else:
        max_height = max(heights)
        images = [
            ImageOps.pad(image, (image.width, max_height), color="white")
            for image in images
        ]

    total_width = sum(image.width for image in images)
    final_width = int(total_width * (scale_percentage / 100))
    final_height = int(max_height * (scale_percentage / 100))

    new_image = Image.new("RGB", (total_width, max_height), (255, 255, 255))

    x_offset = 0
    for image in images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.width

    new_image = new_image.resize((final_width, final_height), Image.Resampling.LANCZOS)

    # Adjust resolution
    if resolution == "Optimised for screen (72 dpi)":
        new_image = new_image.resize(
            (int(new_image.width / 300 * 72), int(new_image.height / 300 * 72)),
            Image.Resampling.LANCZOS,
        )
    elif resolution == "Optimised for print (300 dpi)":
        new_image = new_image.resize(
            (new_image.width, new_image.height), Image.Resampling.LANCZOS
        )

    return new_image


def validate_filename(filename):
    # Separate the base filename and extension
    base, ext = filename.rsplit(".", 1)
    # Check for special characters in the base filename and valid extension
    if re.match(r"^[\w\-]+$", base) and ext in ["jpg", "jpeg"]:
        return True
    return False


def main():
    st.title("Image Stitcher")

    uploaded_files = st.file_uploader(
        "Upload Images", type=["jpg", "jpeg", "png", "gif"], accept_multiple_files=True
    )

    if uploaded_files:
        images = [Image.open(file) for file in uploaded_files]

        st.subheader("Uploaded Images")
        border_width = st.number_input("Border width (pixels):", min_value=0, value=0)

        thumbs = []
        for image in images:
            thumb = image.copy()
            thumb.thumbnail((150, 150), Image.Resampling.LANCZOS)
            if border_width > 0:
                thumb = ImageOps.expand(thumb, border=border_width, fill="white")
            thumbs.append(thumb)

        order = st.text_input(
            "Enter the order of images separated by commas (e.g., 0,1,2 for original order):",
            value=",".join(map(str, range(len(uploaded_files)))),
        )
        order = list(map(int, order.split(",")))

        reordered_images = [images[i] for i in order]
        reordered_thumbs = [thumbs[i] for i in order]

        st.image(
            reordered_thumbs, width=150, caption=[uploaded_files[i].name for i in order]
        )

        st.subheader("Settings")
        pad_or_scale = st.radio(
            "For shorter images:", ["Pad with white rectangle", "Scale to match height"]
        )
        pad_or_scale = "Scale" if pad_or_scale == "Scale to match height" else "Pad"
        scale_percentage = st.slider("Scale Percentage", 1, 200, 100)

        resolution = st.radio(
            "Final Image Resolution:",
            [
                "Original Resolution",
                "Optimised for screen (72 dpi)",
                "Optimised for print (300 dpi)",
            ],
        )

        if resolution == "Original Resolution":
            final_width = sum(image.size[0] for image in reordered_images)
            final_height = max(image.size[1] for image in reordered_images)
        else:
            final_width = int(
                sum(image.size[0] for image in reordered_images)
                * (scale_percentage / 100)
            )
            final_height = int(
                max(image.size[1] for image in reordered_images)
                * (scale_percentage / 100)
            )

        st.write(f"Current target resolution: {final_width} x {final_height} pixels")

        filename = st.text_input(
            "Enter the filename for the stitched image (without extension):",
            value="stitched_image",
        )
        file_extension = st.radio("File Extension:", ["jpg", "jpeg"])

        full_filename = f"{filename}.{file_extension}"

        if st.button("Stitch Images"):
            if validate_filename(full_filename):
                result_image = stitch_images(
                    reordered_images,
                    pad_or_scale,
                    scale_percentage,
                    border_width,
                    resolution,
                )
                st.image(result_image, caption="Stitched Image", use_column_width=True)

                buffer = io.BytesIO()
                result_image.save(buffer, format="JPEG")
                st.download_button(
                    "Download Stitched Image",
                    buffer,
                    file_name=full_filename,
                    mime="image/jpeg",
                )
            else:
                st.error(
                    "Invalid filename. Please use only alphanumeric characters, underscores, and dashes, and ensure the extension is .jpg or .jpeg."
                )


if __name__ == "__main__":
    main()
