import numpy as np
from PIL import Image
import plotly.graph_objects as go
import svgwrite

def create_downsampled_image_array(image_path, downsample_scale):
    # Step 1: Read the PNG file
    image = Image.open(image_path)

    # Step 2: Convert the image to grayscale
    image_gray = image.convert("L")

    # Step 3: Downscale the image into an array of grayscale values
    image_array = np.array(image_gray)

    # Step 4: Create mask to filter out data with grayscale value of 0
    mask = image_array > 0
    masked_image_array = np.where(mask, image_array, np.nan)

    downsampled_image_array = masked_image_array[::downsample_scale]

    # normalize the downsampled image array
    downsampled_image_array = downsampled_image_array / np.nanmax(downsampled_image_array)

    # multiply by 1000 haha
    downsampled_image_array = downsampled_image_array * 1000

    return downsampled_image_array


# create a figure
topographylines = go.Figure()
downsample_scale = 100
LA_downsampled_array = create_downsampled_image_array("./Maps/LA.png", downsample_scale)
Paris_downsampled_array = create_downsampled_image_array("./Maps/Paris.png", downsample_scale)

# create a bunch of topography lines for LA along the image row of the same color and add them to the figure
for idx, row in enumerate(LA_downsampled_array):
    topographylines.add_trace(go.Scatter3d(
        x=idx*np.ones(len(row))*downsample_scale, 
        y=np.arange(len(row)), 
        z=row, 
        mode='lines',
        line=dict(color='blue', width=2)
    ))

# create a bunch of topography lines for Paris along the image row of the same color and add them to the figure
for idx, row in enumerate(Paris_downsampled_array):
    topographylines.add_trace(go.Scatter3d(
        x=idx*np.ones(len(row))*downsample_scale, 
        z=np.arange(len(row)), 
        y=row, 
        mode='lines',
        line=dict(color='red', width=2)
    ))

topographylines.show()

# extract a single row from LA
row = LA_downsampled_array[0]

# convert it into a list of tuples which represent x and y coordinates
coords = []
for idx, value in enumerate(row):
    if not np.isnan(value):
        coords.append((idx, value))


# create a SVG drawing
dwg = svgwrite.Drawing('test.svg', profile='tiny')
dwg.add(dwg.polyline(points=coords, fill='none', stroke='blue', stroke_width=2))
dwg.save()


# create a function that creates a svg for each row in the downsampled array
def create_svg_from_array(array, filename):
    dwg = svgwrite.Drawing(f'{filename}.svg', profile='tiny')
    for idx, row in enumerate(array):
        coords = []
        for idx, value in enumerate(row):
            if not np.isnan(value):
                coords.append((idx, value))
        dwg.add(dwg.polyline(points=coords, fill='none', stroke='blue', stroke_width=2))
    dwg.save()

create_svg_from_array(LA_downsampled_array, 'LA')



