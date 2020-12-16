import numpy as np
import cv2
from numpy import ones, vstack
from numpy.linalg import lstsq
from statistics import mean
from PIL import ImageGrab
from pyberpunk2077cli.env import *


def interest_region(img, vertices):
    # Initialize mask with blank content:
    mask = np.zeros_like(img)

    # Fill mask with white pixels
    cv2.fillPoly(mask, vertices, 255)

    # Returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked


def draw_lanes(img, lines, color=[0, 255, 255], thickness=3):
    if lines is None:
        return
    # if this fails, go with some default line
    try:

        # finds the maximum y value for a lane marker
        # (since we cannot assume the horizon will always be at the same point.)

        ys = []
        for i in lines:
            for ii in i:
                ys += [ii[1], ii[3]]
        min_y = min(ys)
        max_y = 600
        new_lines = []
        line_dict = {}

        for idx, i in enumerate(lines):
            for xyxy in i:
                # http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                x_coords = (xyxy[0], xyxy[2])
                y_coords = (xyxy[1], xyxy[3])
                A = vstack([x_coords, ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords, rcond=None)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y - b) / m
                x2 = (max_y - b) / m

                line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]

            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]

            else:
                found_copy = False

                for other_ms in final_lanes_copy:

                    if not found_copy:
                        if abs(other_ms * 1.2) > abs(m) > abs(other_ms * 0.8):
                            if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(b) > abs(
                                    final_lanes_copy[other_ms][0][1] * 0.8):
                                final_lanes[other_ms].append([m, b, line])
                                found_copy = True
                                break
                        else:
                            final_lanes[m] = [[m, b, line]]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s))

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
    except Exception as e:
        pass


def draw_lines(image):
    # Store original image to be used later
    original_image = image

    # Turn image into gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use canny to get the edges of the image
    processed_img = cv2.Canny(processed_img, threshold1=CANVY_THRESHOLD_1, threshold2=CANVY_THRESHOLD_2)

    processed_img = cv2.GaussianBlur(processed_img, GAUSSIAN_KERNEL, 0)

    vertices = np.array(MASK_VERTICES, np.int32)

    processed_img = interest_region(processed_img, [vertices])

    # https://medium.com/@mrhwick/simple-lane-detection-with-opencv-bfeb6ae54ec0
    lines = cv2.HoughLinesP(processed_img,
                            rho=1,
                            theta=np.pi / 180,
                            threshold=180,
                            lines=np.array([]),
                            minLineLength=LINE_MIN_LENGTH,
                            maxLineGap=LINE_MAX_GAP)
    m1 = 0
    m2 = 0
    # https://pythonprogramming.net/game-frames-open-cv-python-plays-gta-v/
    try:
        l1, l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)
            except Exception as e:
                pass
    except Exception as e:
        pass

    return processed_img, original_image, m1, m2


def get_lanes(lines=False):
    screen = np.array(ImageGrab.grab(bbox=(0, 40, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)))
    new_screen, original_image, m1, m2 = draw_lines(screen)
    cv2.imshow('lanes', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    if lines:
        cv2.imshow('lines', new_screen)
    return m1, m2


def stop_key():
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        return True
    else:
        return False
