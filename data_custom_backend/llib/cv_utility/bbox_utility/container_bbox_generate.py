# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： container_bbox_generate
Description :
Author : 'li'
date： 2020/10/28
-------------------------------------------------
Change Activity:
2020/10/28:
-------------------------------------------------
"""
import time

import cv2
import numpy as np

from llib.cv_utility.bbox_utility.bbox_utility import resort_points
from llib.cv_utility.bbox_utility.draw_line_from_point import draw_line_from_points
from llib.cv_utility.image_opt_utility import read_image, write_image, enlarge_bbox


class ContainerBboxGenerate:
    def __init__(self, text_area_pixel, gap_area_pixel, threshold=0.8, min_bbox_pixel_size=20):
        """
        container bbox generate
        :param text_area_pixel:
        :param gap_area_pixel:
        """
        self.original_textarea_pixel = text_area_pixel
        self.original_gap_area_pixel = gap_area_pixel
        self.threshold = threshold
        self.min_bbox_pixel_size = min_bbox_pixel_size
        self.format_textarea_pixel, self.format_gap_area_pixel = self._format_original_pixel()

    def _format_original_pixel(self):
        """
        format pixel by threshold
        :return:
        """
        area = np.zeros_like(self.original_textarea_pixel, dtype=np.int)
        area[np.where(self.original_textarea_pixel > self.threshold)] = 255
        gap = np.zeros_like(self.original_gap_area_pixel, dtype=np.int)
        gap[np.where(self.original_gap_area_pixel > self.threshold - 0.2)] = 255
        return area, gap

    def gen_bbox(self):
        """

        :return:
        """
        line_points = self._get_gap_lines()
        bg = np.zeros_like(self.original_textarea_pixel, dtype=np.int)
        for point in line_points:
            tmp_canvas = draw_line_from_points(point, bg)
            bg = bg + tmp_canvas
        # write_image('line.jpg', bg * 255)
        bg = self.format_textarea_pixel - bg

        bg[np.where(bg < 0)] = 0
        # write_image('pix.jpg', bg * 255)
        text_area_domain = ContainerBboxGenerate._get_connected_domain(bg)
        bboxes = self._gen_bboxes_by_domain(text_area_domain)
        return bboxes

    @staticmethod
    def _get_single_by_domain(domain):
        """
        domain
        :param domain:
        :return:
        """
        ret, thresh = cv2.threshold(domain, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return None
        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = resort_points(box)
        return box

    def _gen_bboxes_by_domain(self, domain):
        """
        gen bboxes by domain
        :param domain:
        :return:
        """
        domain_max_value = domain.max()
        bboxes = []
        for i in range(1, domain_max_value + 1):
            locations = np.where(domain == i)
            if locations[0].size < self.min_bbox_pixel_size:
                continue
            bg = np.zeros_like(domain, dtype=np.uint8)
            bg[locations] = 255
            bbox = ContainerBboxGenerate._get_single_by_domain(bg)
            if bbox is not None:
                bbox = np.array(enlarge_bbox(1, bbox, domain.shape))
                bboxes.append(bbox * 2)

        return bboxes

    def _get_gap_lines(self):
        """
        gen gap line from gap area
        :return:
        """
        intersection_area = self._get_intersection_area()
        intersection_domain = ContainerBboxGenerate._get_connected_domain(intersection_area)
        gap_domain = ContainerBboxGenerate._get_connected_domain(self.format_gap_area_pixel)
        domain_max_value = intersection_domain.max()
        if domain_max_value == 0:
            return []
        gap_lines = []
        for i in range(1, domain_max_value + 1):  # for each domain
            xs, ws = np.where(intersection_domain == i)
            x, y = xs[0], ws[0]
            domain_value = gap_domain[x, y]
            selected_domain_area = np.zeros_like(gap_domain, dtype=np.uint8)
            selected_domain_area[np.where(gap_domain == domain_value)] = 255
            points = ContainerBboxGenerate._gen_bbox_by_domain(selected_domain_area)
            # points = (np.array([points[0][0], points[0][1] + 1]), np.array([points[1][0], points[1][1] + 1]))
            gap_lines.append(points)
        return gap_lines

    def _get_intersection_area(self):
        """
        get intersection area
        :return:
        """
        tmp_area = self.format_textarea_pixel + self.format_gap_area_pixel
        intersection_area = np.zeros_like(tmp_area, np.uint8)
        intersection_area[np.where(tmp_area > 300)] = 255
        return intersection_area

    @staticmethod
    def _get_connected_domain(intersection_area):
        """
        get connected domain
        :param intersection_area:
        :return:
        """
        tmp_area = intersection_area.astype(np.uint8)
        _, labels_image = cv2.connectedComponents(tmp_area, connectivity=4)
        return labels_image

    @staticmethod
    def _gen_bbox_by_domain(selected_domain_area):
        ret, thresh = cv2.threshold(selected_domain_area, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = resort_points(box)
        point_1, point_2 = (box[0] + box[3]) / 2, (box[1] + box[2]) / 2
        return point_1.astype(np.int), point_2.astype(np.int)


def main():
    for i in range(10):
        start_time = time.time()
        text_area = read_image('imgs/txt.jpg')
        gap_area = read_image('imgs/gap.jpg')
        bbox_generator = ContainerBboxGenerate(text_area / 255, gap_area / 255)
        bbox_generator.gen_bbox()
        print(time.time() - start_time)


if __name__ == '__main__':
    main()
