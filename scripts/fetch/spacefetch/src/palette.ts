// The Caelestia dynamic scheme: the colors Caelestia derives from the current
// wallpaper. Spacefetch draws its own panel instead of going through
// ~/.config/fastfetch/config.jsonc, so it reads the scheme directly at run
// time; the colors then follow the wallpaper with no re-render step.
import { readFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { mix, type Ramp } from './color'

/** Panel text, using the same roles the fastfetch box took from the scheme. */
const VALUE_KEY = 'onSurface'
const MUTED_KEY = 'onSurfaceVariant'

/** Which scheme color tints each body, keeping the six zones distinct. */
const ZONE_KEY: Record<string, string> = {
  sun: 'yellow',
  rocky: 'maroon',
  gas: 'peach',
  ice: 'blue',
  comet: 'mauve',
  hole: 'red',
}

const SCHEME_PATH =
  process.env.CAELESTIA_SCHEME_PATH ?? join(homedir(), '.local/state/caelestia/scheme.json')

let colours: Record<string, number> | null = null

/** 0xRRGGBB from "bac5ee" (with or without '#'), the form the scheme uses. */
function parseHex(value: unknown): number | null {
  const match = typeof value === 'string' ? /^#?([0-9a-f]{6})$/i.exec(value.trim()) : null

  return match ? Number.parseInt(match[1]!, 16) : null
}

function readColours(raw: Record<string, unknown>): Record<string, number> {
  const out: Record<string, number> = {}
  for (const [key, value] of Object.entries(raw)) {
    const parsed = parseHex(value)
    if (parsed !== null) out[key] = parsed
  }

  return out
}

/**
 * The live scheme, or null when nothing readable is found — in which case
 * spacefetch keeps its own built-in colors.
 *
 * $SCHEME_COLOURS (what Caelestia exports to a theme post-hook) wins, matching
 * render.py; otherwise ~/.local/state/caelestia/scheme.json is read.
 */
export function loadScheme(): Record<string, number> | null {
  const fromEnv = process.env.SCHEME_COLOURS
  if (fromEnv) {
    try {
      colours = readColours(JSON.parse(fromEnv) as Record<string, unknown>)
      if (Object.keys(colours).length > 0) return colours
    } catch {
      // Not JSON: fall through to the file rather than giving up on the scheme.
    }
  }

  try {
    const parsed = JSON.parse(readFileSync(SCHEME_PATH, 'utf8')) as { colours?: Record<string, unknown> }
    colours = readColours(parsed.colours ?? (parsed as Record<string, unknown>))
  } catch {
    colours = null
  }

  return colours !== null && Object.keys(colours).length > 0 ? colours : null
}

/** A scheme color by name, or the caller's fallback when the scheme lacks it. */
export function schemeColour(key: string, fallback: number): number {
  return colours?.[key] ?? fallback
}

/** The scheme color that tints a body. */
export function zoneKey(body: string): string {
  return ZONE_KEY[body] ?? 'primary'
}

export function textValue(): number {
  return schemeColour(VALUE_KEY, 0xd8d8e0)
}

export function textMuted(): number {
  return schemeColour(MUTED_KEY, 0x8a8a96)
}

/**
 * How the body and the sky are painted: the scheme's background at the bottom,
 * the zone's color through the middle, and a lift toward the scheme's text at
 * the top. The art's own brightness survives, so the shading and the depth
 * stay; the hue becomes the wallpaper's.
 */
export function artRamp(accent: number): Ramp {
  return {
    low: schemeColour('background', 0x000000),
    mid: accent,
    high: mix(accent, schemeColour(VALUE_KEY, 0xffffff), 0.65),
  }
}
