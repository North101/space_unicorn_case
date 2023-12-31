import argparse
import pathlib
from typing import TypedDict

from .shared import *


class SpaceArgs(TypedDict):
  width: float
  height: float
  led_columns: float
  led_rows: float
  mounting_offset_x: float
  mounting_offset_y: float
  usb_center_offset_y: float
  usb_width: float
  usb_height: float


def add_space_args(
    parent: argparse._SubParsersAction,
    name: str,
    args: SpaceArgs | None = None,
):
  parser = parent.add_parser(name)
  parser.add_argument('--output',
                      type=pathlib.Path, default='output', help='output path')
  if args is None:
    parser.add_argument('--width',
                        type=float, required=True, help='width (mm)')
    parser.add_argument('--height',
                        type=float, required=True, help='height (mm)')
  parser.add_argument('--depth',
                      type=float, default=15, help='depth (mm)')
  parser.add_argument('--thickness',
                      type=float, default=3.17, help='wood thickness (mm)')
  parser.add_argument('--kerf',
                      type=float, default=0.08, help='kerf (mm)')

  parser.add_argument('--tab',
                      type=float, default=10, help='tab size (mm)')
  parser.add_argument('--depth-tab',
                      type=float, default=7.5, help='depth tab size (mm)')

  if args is None:
    parser.add_argument('--led_columns',
                        type=int, required=True)
    parser.add_argument('--led_rows',
                        type=int, required=True)
    parser.add_argument('--mounting_offset_x',
                        type=float, required=True)
    parser.add_argument('--mounting_offset_y',
                        type=float, required=True)
    parser.add_argument('--usb_center_offset_y',
                        type=float, required=True)
    parser.add_argument('--usb_width',
                        type=float, required=True)
    parser.add_argument('--usb_height',
                        type=float, required=True)
  else:
    parser.set_defaults(**args)


def parse_args():
  parser = argparse.ArgumentParser(prog='space_unicorn_case')
  subparsers = parser.add_subparsers(required=True)

  add_space_args(subparsers, 'galactic', args=SpaceArgs(
      width=330,
      height=78,
      mounting_offset_x=108,
      mounting_offset_y=72,
      led_columns=53,
      led_rows=11,
      usb_center_offset_y=12,
      usb_width=3,
      usb_height=15,
  ))

  add_space_args(subparsers, 'cosmic', args=SpaceArgs(
      width=204,
      height=204,
      mounting_offset_x=99,
      mounting_offset_y=99,
      led_columns=32,
      led_rows=32,
      usb_center_offset_y=12,
      usb_width=3,
      usb_height=15,
  ))

  add_space_args(subparsers, 'stellar', args=SpaceArgs(
      width=108,
      height=108,
      mounting_offset_x=102,
      mounting_offset_y=102,
      led_columns=16,
      led_rows=16,
      usb_center_offset_y=12,
      usb_width=3,
      usb_height=15,
  ))

  add_space_args(subparsers, 'custom')

  return parser.parse_args()


def main():
  args = parse_args()
  svgs = write_all_svg(args=SVGArgs(
      output=args.output,
      width=args.width,
      height=args.height,
      depth=args.depth,
      thickness=args.thickness,
      kerf=args.kerf,
      tab=args.tab,
      depth_tab=args.depth_tab,
      mounting_offset_x=args.mounting_offset_x,
      mounting_offset_y=args.mounting_offset_y,
      led_rows=args.led_rows,
      led_columns=args.led_columns,
      usb_width=args.usb_width,
      usb_height=args.usb_height,
      usb_center_offset_y=args.usb_center_offset_y,
  ))

  data = [
      (str(filename), str(svg.attrs.width), str(svg.attrs.height))
      for (filename, svg) in svgs
  ]
  name_len = max(len(name) for (name, _, _) in data)
  width_len = max(len(width) for (_, width, _) in data)
  height_len = max(len(height) for (_, _, height) in data)
  for (name, width, height) in data:
    print(f'{name:<{name_len}} @ {width:>{width_len}} x {height:>{height_len}}')


if __name__ == '__main__':
  main()
