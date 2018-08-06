def re_map(value, min_input, max_input, min_output, max_output):
    value = max_input if value > max_input else value
    value = min_input if value < min_input else value

    input_span = max_input - min_input
    output_span = max_output - min_output

    scaled_thrust = float(value - min_input) / float(input_span)

    return min_output + (scaled_thrust * output_span)
