/** Colors as 0xRRGGBB, and the escapes that paint them. */

/**
 * Mono mode (`--mono`): every escape is emitted as a grey of the same
 * luminance, so the body, the sky and the panel all come out black and white.
 * Both `fg` and `bg` funnel through here, so this is the one place to flip.
 */
let mono = false

/** Where the body and the sky sit on the scheme, as `low` -> `mid` -> `high`. */
export type Ramp = { low: number; mid: number; high: number }

/** Set from the Caelestia scheme; null leaves the art in its own colors. */
let ramp: Ramp | null = null

export function setMono(value: boolean): void {
  mono = value
}

export function setRamp(value: Ramp | null): void {
  ramp = value
}

export function clamp(value: number, low: number, high: number): number {
  return Math.max(low, Math.min(high, value))
}

function channels(color: number): [number, number, number] {
  return [(color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff]
}

/** Rec. 709 luma: keeps each color's brightness when the hue goes. */
function grey(color: number): number {
  const [r, g, b] = channels(color)
  const luma = Math.round(0.2126 * r + 0.7152 * g + 0.0722 * b)

  return (luma << 16) | (luma << 8) | luma
}

/**
 * Re-paints a color through the scheme ramp by its brightness: dark art lands
 * near the background, midtones on the accent, highlights near the text. The
 * shading survives, so the body keeps its form and loses only its own hue.
 */
function ramped(color: number, { low, mid, high }: Ramp): number {
  const [r, g, b] = channels(color)
  const luma = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255

  return luma < 0.5 ? mix(low, mid, luma * 2) : mix(mid, high, (luma - 0.5) * 2)
}

/** `art` picks up the scheme ramp; the panel already speaks in scheme colors. */
function painted(color: number, art: boolean): [number, number, number] {
  let value = art && ramp !== null ? ramped(color, ramp) : color
  if (mono) value = grey(value)

  return channels(value)
}

export function rgb(r: number, g: number, b: number): number {
  return (Math.round(clamp(r, 0, 255)) << 16) | (Math.round(clamp(g, 0, 255)) << 8) | Math.round(clamp(b, 0, 255))
}

export function mix(from: number, to: number, k: number): number {
  const a = channels(from)
  const b = channels(to)
  const w = clamp(k, 0, 1)

  return rgb(a[0] + (b[0] - a[0]) * w, a[1] + (b[1] - a[1]) * w, a[2] + (b[2] - a[2]) * w)
}

export function shade(color: number, k: number): number {
  const [r, g, b] = channels(color)

  return rgb(r * k, g * k, b * k)
}

/** Body and sky: tinted into the scheme, then greyscaled if `--mono`. */
export function fg(color: number): string {
  const [r, g, b] = painted(color, true)

  return `\x1b[38;2;${r};${g};${b}m`
}

export function bg(color: number): string {
  const [r, g, b] = painted(color, true)

  return `\x1b[48;2;${r};${g};${b}m`
}

/**
 * The panel: left off the ramp, because its colors are read from the scheme
 * already and running them through it a second time would only fade them.
 */
export function fgFlat(color: number): string {
  const [r, g, b] = painted(color, false)

  return `\x1b[38;2;${r};${g};${b}m`
}

export const RESET = '\x1b[0m'
export const BOLD = '\x1b[1m'
