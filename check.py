# Check if all pixels in the 'frame' image are equal to corresponding pixels in the 'original_frame_no_rectangles' image
are_all_pixels_equal = all((pixel1 == pixel2).all(
) for pixel1, pixel2 in zip(frame, original_frame_no_rectangles))

# are_all_pixels_equal will be True if all pixels in 'frame' match corresponding pixels in 'original_frame_no_rectangles',
# and False otherwise

# So, (pixel1 == pixel2).all() evaluates the truth value of the entire array resulting from the element-wise comparison, not individual elements.
if not are_all_pixels_equal:
    status = 1
