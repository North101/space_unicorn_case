import pathlib

from pysvg import circle, g, length, path, rect, svg, transforms

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  width = args.width + (args.thickness * 2)
  height = args.height + (args.thickness * 2)

  top_path = path.d([
      path.placeholder(lambda w, h: path.d.h((width - w) / 2)),
      args.h_tabs(args.tab, args.width, False),
      path.placeholder(lambda w, h: path.d.h((width - w) / 2)),
  ])

  right_path = path.d([
      path.placeholder(lambda w, h: path.d.v((height - h) / 2)),
      args.v_tabs(args.tab, args.height, False),
      path.placeholder(lambda w, h: path.d.v((height - h) / 2)),
  ])

  bottom_path = -top_path

  left_path = -right_path

  d = path.d([
      path.d.m(0, 0),
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
          g(
              attrs=g.attrs(
                  transform=transforms.translate(
                      round(args.thickness + args.mounting_x, 2),
                      round(args.thickness + args.mounting_y, 2),
                  ),
              ) | args.cut,
              children=[
                  circle(attrs=circle.attrs(
                      cx=round(x * args.mounting_offset_x, 2),
                      cy=round(y * args.mounting_offset_y, 2),
                      r=round(1 + args.kerf, 2),
                  ))
                  for x in range(4)
                  for y in range(2)
              ],
          ),
          g(
              attrs=g.attrs(
                  transform=transforms.translate(
                      round(args.thickness + 5, 2),
                      round(args.thickness + 5, 2),
                  ),
              ),
              children=[
                  rect(attrs=rect.attrs(
                      width=round(args.width - 10, 2),
                      height=round(args.height - 10, 2),
                      rx=2.5,
                      ry=2.5,
                  ) | args.cut),
              ],
          )
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
