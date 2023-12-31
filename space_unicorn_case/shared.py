import math
import pathlib
from typing import NamedTuple, Protocol

from pysvg import PresentationAttributes, path, svg


class SVGArgs(NamedTuple):
  output: pathlib.Path
  width: float
  height: float
  depth: float
  thickness: float
  kerf: float
  tab: float
  depth_tab: float

  led_columns: int
  led_rows: int

  mounting_offset_x: float
  mounting_offset_y: float

  usb_center_offset_y: float
  usb_width: float
  usb_height: float

  led_x: float = 6.5
  led_y: float = 6.5
  led_width: float = 5
  led_height: float = 5
  led_offset_x: float = 6
  led_offset_y: float = 6

  mounting_x: float = 3
  mounting_y: float = 3

  def h_tab_half(self, tab):
    return path.d.h(tab / 2)

  def h_tab(self, tab: float, out: bool):
    kerf = -self.kerf if out else self.kerf
    thickness = -path.d.v(self.thickness) if out else path.d.v(self.thickness)
    return path.d([
        path.d.h((tab / 2) + kerf),
        thickness,
        path.d.h(tab + -kerf + -kerf),
        -thickness,
        path.d.h(kerf + (tab / 2)),
    ])

  def h_tabs(self, tab: float, width: float, out: bool):
    h_tab = self.h_tab(tab, out)
    count = math.floor(width / h_tab.width)
    return path.d([
        h_tab
        for _ in range(count)
    ])

  def v_tab_half(self, tab):
    return path.d.v(tab / 2)

  def v_tab(self, tab: float, out: bool):
    kerf = -self.kerf if out else self.kerf
    thickness = -path.d.h(self.thickness) if out else path.d.h(self.thickness)
    return path.d([
        path.d.v((tab / 2) + kerf),
        -thickness,
        path.d.v(tab + -kerf + -kerf),
        thickness,
        path.d.v(kerf + (tab / 2)),
    ])

  def v_tabs(self, tab: float, height: float, out: bool):
    v_tab = self.v_tab(tab, out)
    count = math.floor(height / v_tab.height)
    return path.d([
        v_tab
        for _ in range(count)
    ])

  cut = PresentationAttributes(
      fill='none',
      stroke='black',
      stroke_width=0.001,
  )

  engrave = PresentationAttributes(
      fill='black',
      stroke='none',
      stroke_width=0.001,
  )


class RegisterSVGCallable(Protocol):
  def __call__(self, args: SVGArgs) -> tuple[pathlib.Path, svg]:
    ...


svg_list: list[RegisterSVGCallable] = []


def register_svg(f: RegisterSVGCallable):
  svg_list.append(f)
  return f


def write_all_svg(args: SVGArgs):
  args.output.mkdir(parents=True, exist_ok=True)
  data = [
      write_svg(args)
      for write_svg in svg_list
  ]
  for (filename, svg_data) in data:
    filename.write_text(str(svg_data))

  return data
