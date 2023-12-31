import pathlib

from pysvg import circle, g, length, rect, svg, transforms

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  s = svg(
      attrs=svg.attrs(
          width=length(round(args.width, 2), 'mm'),
          height=length(round(args.height, 2), 'mm'),
          viewBox=(0, 0, round(args.width, 2), round(args.height, 2)),
      ),
      children=[
          rect(attrs=rect.attrs(
              width=round(args.width, 2),
              height=round(args.height, 2),
              rx=2.5,
              ry=2.5,
          ) | args.cut),
          g(
              attrs=g.attrs(
                  transform=transforms.translate(
                      round(args.mounting_x, 2),
                      round(args.mounting_y, 2),
                  ),
              ) | args.cut,
              children=[
                  circle(attrs=circle.attrs(
                      cx=round(x * args.mounting_offset_x, 2),
                      cy=round(y * args.mounting_offset_y, 2),
                      r=round(1 + args.kerf, 2),
                  ))
                  for x in range(math.floor(args.width / args.mounting_offset_x) + 1)
                  for y in range(math.floor(args.height / args.mounting_offset_y) + 1)
              ],
          ),
          g(
              attrs=g.attrs(
                  transform=transforms.translate(
                      round(args.led_x, 2),
                      round(args.led_y, 2),
                  ),
              ) | args.engrave,
              children=[
                  rect(attrs=rect.attrs(
                      x=round(x * args.led_offset_x, 2),
                      y=round(y * args.led_offset_y, 2),
                      width=args.led_width,
                      height=args.led_height,
                  ))
                  for x in range(args.led_columns)
                  for y in range(args.led_rows)
              ],
          ),
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
