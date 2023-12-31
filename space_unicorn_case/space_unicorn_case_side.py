import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg_with_usb(args: SVGArgs):
  return write_svg_(args, usb=True)


@register_svg
def write_svg_without_usb(args: SVGArgs):
  return write_svg_(args, usb=False)


def write_svg_(args: SVGArgs, usb: bool):
  height = args.height + (args.thickness * 2)
  depth = args.depth + (args.thickness * 2)

  top_path = path.d([
      path.placeholder(lambda w, h: path.d.h((depth - w) / 2)),
      args.h_tabs(args.depth_tab, args.depth, False),
      path.placeholder(lambda w, h: path.d.h((depth - w) / 2)),
  ])

  right_tab = path.d([
      path.placeholder(lambda w, h: path.d.v((depth - h) / 2)),
      args.v_tabs(args.depth_tab, args.depth, False),
      path.placeholder(lambda w, h: path.d.v((depth - h) / 2)),
  ])

  right_path = path.d([
      path.d.v(args.thickness),
      right_tab,
      path.placeholder(lambda w, h: path.d.v(height - h)),
  ])

  bottom_path = -top_path

  left_path = path.d([
      -path.placeholder(lambda w, h: path.d.v((height - h) / 2)),
      -args.v_tabs(args.tab, args.height, True),
      -path.placeholder(lambda w, h: path.d.v((height - h) / 2)),
  ])

  d = path.d([
      path.d.m(args.thickness, 0),
      top_path,
      right_path,
      bottom_path,
      left_path,
      path.d.z(),
  ])

  hole_width = args.depth - 4
  hole_height = args.height - 6

  s = svg(
      attrs=svg.attrs(
          width=length(round(d.width, 2), 'mm'),
          height=length(round(d.height, 2), 'mm'),
          viewBox=(0, 0, round(d.width, 2), round(d.height, 2)),
      ),
      children=[
          path(attrs=path.attrs(
              d=d,
          ) | args.cut),
          path(attrs=path.attrs(
              d=path.d([
                  path.d.m(
                      x=round(args.thickness + 5, 2),
                      y=round((d.height - hole_height + 5) / 2, 2),
                  ),
                  path.d.c(0, 0, 0, -2.5, 2.5, -2.5),
                  path.d.h(round(hole_width - 5, 2)),
                  path.d.c(0, 0, 2.5, 0, 2.5, 2.5),
                  path.d.v(round(hole_height - 5, 2)),
                  path.d.c(0, 0, 0, 2.5, -2.5, 2.5),
                  -path.d.h(round(hole_width - 5, 2)),
                  path.d.c(0, 0, -2.5, 0, -2.5, -2.5),
                  (
                    path.d([
                        -path.d.v(args.usb_center_offset_y - (args.usb_height / 2)),
                        -path.d.h(args.usb_width),
                        -path.d.v(args.usb_height),
                        path.d.h(args.usb_width),
                        -path.placeholder(lambda w, h: path.d.v(hole_height - 5 - h))
                    ])
                    if usb else
                    -path.d.v(round(hole_height - 5, 2))
                  ),
                  path.d.z(),
              ]),
          ) | args.cut),
      ],
  )

  stem = pathlib.Path(__file__).stem
  filename = args.output / pathlib.Path(f'{stem}{'_usb' if usb else ''}').with_suffix('.svg').name
  return filename, s
