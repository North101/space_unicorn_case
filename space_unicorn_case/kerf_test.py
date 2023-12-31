import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  tab_out = path.d([
      path.d.m(0, 0),
      path.d.h(10),
      args.v_tab_half(5),
      args.v_tab(5, True),
      args.v_tab(5, True),
      args.v_tab_half(5),
      -path.d.h(10),
      -path.placeholder(lambda w, h: path.d.v(h)),
  ])

  tab_in = path.d([
      path.d.m(10 + args.tab + 2, 0),
      path.d.h(10),
      args.v_tab_half(5),
      args.v_tab(5, False),
      args.v_tab(5, False),
      args.v_tab_half(5),
      -path.d.h(10),
      -path.placeholder(lambda w, h: path.d.v(h)),
  ])

  d = path.d([
      tab_out,
      tab_in,
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
      ]
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
