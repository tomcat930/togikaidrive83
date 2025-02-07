#!/usr/bin/env python3
# coding: utf-8

import argparse
# import threading
import time
import cv2

from lib.oakd_yolo import OakdYolo

detection_label = None  # 認識結果格納用
detections = []  # 認識結果格納用


def main() -> None:
    end = False
    while not end:
        oakd_yolo = OakdYolo(args.config, args.model,
                             args.fps, save_fps=args.save_fps)
        global labels
        global detections
        labels = oakd_yolo.get_labels()

        while True:
            frame = None
            try:
                frame, detections = oakd_yolo.get_frame()

            except BaseException:
                print("===================")
                print("get_frame() error! Reboot OAK-D.")
                print("If reboot occur frequently, Bandwidth may be too much.")
                print("Please lower FPS.")
                print("==================")
                break
            if frame is not None:
                oakd_yolo.display_frame("nn", frame, detections)
            if cv2.waitKey(1) == ord("q"):
                end = True
                break
        oakd_yolo.close()


if __name__ == "__main__":
    # 引数設定(認識モデルのパス設定など)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--model",
        help="Provide model name or model path for inference",
        # default="yolov7tiny_coco_416x416",
        # default="models/aicar_20240825.blob",
        default="models/aicar_20240908.blob",
        type=str,
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Provide config path for inference",
        # default="json/yolov7tiny_coco_416x416.json",
        # default="json/aicar_20240825.json",
        default="json/aicar_20240908.json",
        type=str,
    )
    parser.add_argument(
        "-f",
        "--fps",
        help="Camera frame fps. This should be smaller than nn inference fps",
        default=10,
        type=int,
    )
    parser.add_argument(
        "-s",
        "--save_fps",
        help="Image save fps. If it's > 0, images and video will be saved.",
        default=0,
        type=int,
    )
    args = parser.parse_args()

    main()
