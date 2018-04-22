import numpy


class PatternAnalyser:

    UNKNOWN_PATTERN = "?"

    # returns the starting and ending index of the pattern if it's found
    # supported patterns:
    # W, M, N and V (ex: for macd)
    # return boolean (pattern found or not), start index and end index
    @staticmethod
    def find_pattern(data_frame, zero_crossing_indexes, data_frame_max_index):
        if len(zero_crossing_indexes) > 1:

            last_move_data = data_frame[zero_crossing_indexes[-1]:]

            # if last_move_data is shaped in W
            shape = PatternAnalyser.get_pattern(last_move_data)

            if shape == "N" or shape == "V":
                # check presence of W or M with insignificant move in the other direction
                backwards_index = 2
                while backwards_index < len(zero_crossing_indexes) and \
                        zero_crossing_indexes[-1*backwards_index] - zero_crossing_indexes[-1*backwards_index-1] < 4:
                    backwards_index += 1
                extended_last_move_data = data_frame[zero_crossing_indexes[-1*backwards_index]:]
                extended_shape = PatternAnalyser.get_pattern(extended_last_move_data)

                if extended_shape == "W" or extended_shape == "M":
                    # check that values are on the same side (< or >0)
                    first_part = data_frame[zero_crossing_indexes[-1*backwards_index]:
                                            zero_crossing_indexes[-1*backwards_index+1]]
                    second_part = data_frame[zero_crossing_indexes[-1]:]
                    if numpy.mean(first_part)*numpy.mean(second_part) > 0:
                        return extended_shape, zero_crossing_indexes[-1*backwards_index], zero_crossing_indexes[-1]

            if shape != PatternAnalyser.UNKNOWN_PATTERN:
                return shape, zero_crossing_indexes[-1], data_frame_max_index

        return PatternAnalyser.UNKNOWN_PATTERN, None, None

    @staticmethod
    def get_pattern(data_frame):
        mean_value = numpy.mean(data_frame)*0.5
        indexes_under_mean_value = data_frame.index[data_frame > mean_value] \
            if mean_value < 0 \
            else data_frame.index[data_frame < mean_value]

        nb_gaps = 0
        for i in range(len(indexes_under_mean_value)-1):
            if indexes_under_mean_value[i+1]-indexes_under_mean_value[i] > 3:
                nb_gaps += 1

        if nb_gaps > 1:
            return "W" if mean_value < 0 else "M"
        else:
            return "V" if mean_value < 0 else "N"

    # returns a value 0 < value < 1: the higher the stronger is the pattern
    @staticmethod
    def get_pattern_strength(pattern):
        if pattern == "W" or pattern == "M":
            return 1
        elif pattern == "N" or pattern == "V":
            return 0.75
        return 0
