import numpy as np
import cv2
black_lines = {}
final_vert_scanlines = np.array((0,0,0), np.uint8)

def verticalScanLines(img):

    boundary = []
    for i in range(0, img.shape[1], 5):
        for j in range(0, img.shape[0]):
            boundary_found = False
            while img[j, i][0] == 0 and img[j,i][1] == 0 and img[j, i][2] == 255:
                boundary_found = True
                j += 1
            if boundary_found:
                boundary.append((i, j))

    counter = 0
    global black_lines

    for i in range(0, img.shape[1], 5):
        if any(b[0] == i for b in boundary):
            start_height = filter(lambda x: x[0] == i, boundary)[0][1]
            for j in range(start_height, img.shape[0]):
                px = img[j, i]
                if px[0] == 255 and px[1] == 255 and px[2] == 255:
                    if black_lines.has_key(i):
                        if j == black_lines.get(i)[-1][1] + 1:
                            black_lines[i][-1] = (black_lines.get(i)[-1][0], j)
                        else:
                            black_lines[i].append((j, j))
                    else:
                        black_lines[i] = [(j, j)]
                    img[j, i] = [0, 0, 0]

        else:
            for j in range(0, img.shape[0]):
                px = img[j, i]
                if px[0] == 255 and px[1] == 255 and px[2] == 255:
                    counter += 1
                    img[j, i] = [0, 0, 0]

    global final_vert_scanlines
    final_vert_scanlines = np.array(img)

    return img

def criterion1(img):

    global black_lines, final_vert_scanlines

    for k in black_lines.keys():
        for start, end in black_lines[k]:
            px_top = img[max(0, start - 1), k]
            if end == img.shape[0] - 1:
                if px_top[0] != 0 or px_top[1] != 255 or px_top[2] != 0:
                    black_lines[k].remove((start, end))
                    if black_lines[k].__len__() == 0:
                        black_lines.__delitem__(k)

                    img = cv2.line(img, (k, start), (k, min(end + 1, img.shape[0])), (0, 140, 255), 2)
                    for j in range(start, end):
                        # img[j, k] = [0, 140, 255]
                        final_vert_scanlines[j, k] = [255, 255, 255]

            else:
                px_end = img[end + 1, k]
                if px_top[0] != 0 or px_top[1] != 255 or px_top[2] != 0 \
                        or px_end[0] != 0 or px_end[1] != 255 or px_end[2] != 0:
                    black_lines[k].remove((start, end))
                    if black_lines[k].__len__() == 0:
                        black_lines.__delitem__(k)

                    img = cv2.line(img, (k, start), (k, min(end + 1, img.shape[0])), (0, 140, 255), 2)
                    for j in range(start, end + 1):
                        # img[j, k] = [0, 140, 255]

                        final_vert_scanlines[j, k] = [255, 255, 255]

    return img

def criterion2(img):

    global black_lines, final_vert_scanlines

    for k in black_lines.keys():
        for start, end in black_lines[k]:
            start2 = start + 1
            end2 = end - 1
            if k == 0:
                for j in range(start2, end2):
                    px_right = img[j, k+1]
                    if px_right[0] != 255 or px_right[1] != 255 or px_right[2] != 255:
                        black_lines[k].remove((start, end))
                        if black_lines[k].__len__() == 0:
                            black_lines.__delitem__(k)

                        img = cv2.line(img, (k, start), (k, min(end + 1, img.shape[0])), (255, 0, 255), 2)
                        for j in range(start, min(end + 1, img.shape[0])):
                            # img[j, k] = [255, 0, 255]
                            final_vert_scanlines[j, k] = [255, 255, 255]
            elif k == img.shape[1] - 1:
                for j in range(start2, end2):
                    px_left = img[j, k - 1]
                    if px_left[0] != 255 or px_left[1] != 255 or px_left[2] != 255:
                        black_lines[k].remove((start, end))
                        if black_lines[k].__len__() == 0:
                            black_lines.__delitem__(k)

                        img = cv2.line(img, (k, start), (k, min(end + 1, img.shape[0])), (255, 0, 255), 2)
                        for j in range(start, min(end + 1, img.shape[0])):
                            # img[j, k] = [255, 0, 255]
                            final_vert_scanlines[j, k] = [255, 255, 255]
            else:
                for j in range(start2, end2):
                    px_left = img[j, k - 1]
                    px_right = img[j, k + 1]
                    if px_right[0] != 255 or px_right[1] != 255 or px_right[2] != 255 \
                            or px_left[0] != 255 or px_left[1] != 255 or px_left[2] != 255:
                        if black_lines.has_key(k):
                            if black_lines[k].__contains__((start, end)):
                                black_lines[k].remove((start, end))
                            if black_lines[k].__len__() == 0:
                                black_lines.__delitem__(k)

                        img = cv2.line(img, (k, start), (k, min(end + 1, img.shape[0])), (255, 0, 255), 2)
                        for j in range(start, min(end + 1, img.shape[0])):
                            # img[j, k] = [255, 0, 255]
                            final_vert_scanlines[j, k] = [255, 255, 255]

    return img

def criterion3(img):

    global black_lines, final_vert_scanlines
    sum = 0
    counter = 0
    for k in black_lines.keys():
        for start, end in black_lines[k]:
            if abs(start - end) > 3:
                sum += abs(start - end)
                counter += 1

    avg = 2 * (sum/counter)
    for k in black_lines.keys():
        for start, end in black_lines[k]:
            if abs(start - end) > avg:
                black_lines[k].remove((start, end))
                if black_lines[k].__len__() == 0:
                    black_lines.__delitem__(k)

                img = cv2.line(img, (k, start), (k, min(end+1, img.shape[0])), (255, 255, 0), 2)
                for j in range(start, min(end + 1, img.shape[0])):
                    # img[j, k] = [255, 0, 0]
                    final_vert_scanlines[j, k] = [255, 255, 255]

    return img

def criterion4(img):

    global black_lines, final_vert_scanlines
    for k in black_lines.keys():
        k_range = []
        if k == 0:
            k_range = range(5, 20, 5)
        elif k == 5:
            k_range = [0, 10, 15]
        elif k == img.shape[1] - 1:
            k_range = range(img.shape[1] - 16, img.shape[1] - 1, 5)
        elif k == img.shape[1] - 6:
            k_range = [img.shape[1] - 16, img.shape[1] - 11, img.shape[1] - 1]
        else:
            k_range = [k - 10, k - 5, k + 5, k + 10]

        for start, end in black_lines[k]:
            counter = 0
            for ki in k_range:
                if black_lines.keys().__contains__(ki):
                    for neighbor_start, neighbor_end in black_lines[ki]:
                        found_in_line = False
                        # print "Checking if [", neighbor_start, ",", neighbor_end,"] is inline with [",start,",",end,"]"
                        for height_value in range(neighbor_start, neighbor_end + 1):
                            if start <= height_value <= end:
                                counter += 1
                                found_in_line = True
                                break
                        if found_in_line:
                            break

            if counter < 3:
                black_lines[k].remove((start, end))
                if black_lines[k].__len__() == 0:
                    black_lines.__delitem__(k)
                img = cv2.line(img, (k, start), (k, min(end+1, img.shape[0])), (0, 255, 225), 2)
                for j in range(start, end + 1):
                    # img[j, k] = [0, 255, 255]
                    final_vert_scanlines[j, k] = [255, 255, 255]

    return img

def final_scanlines():
    global final_vert_scanlines
    return final_vert_scanlines


