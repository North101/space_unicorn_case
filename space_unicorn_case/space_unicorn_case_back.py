import pathlib

from pysvg import circle, length, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  width = args.width
  depth = args.depth + (args.thickness * 2)

  top_path = path.d([
      path.placeholder(lambda w, h: path.d.h((width - w) / 2)),
      args.h_tabs(args.tab, args.width, True),
      path.placeholder(lambda w, h: path.d.h((width - w) / 2)),
  ])

  right_path = path.d([
      path.placeholder(lambda w, h: path.d.v((depth - h) / 2)),
      args.v_tabs(args.depth_tab, args.depth, True),
      path.placeholder(lambda w, h: path.d.v((depth - h) / 2)),
  ])

  bottom_path = -path.d.h(width)

  left_path = -right_path

  d = path.d([
      path.d.m(args.thickness, args.thickness),
      top_path,
      right_path,
      bottom_path,
      left_path,
      path.d.z(),
  ])

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
          circle(attrs=circle.attrs(
              cx=d.width / 2,
              cy=args.thickness + ((d.height - args.thickness) / 2),
              r=2.5 + args.kerf,
          ) | args.cut),
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
