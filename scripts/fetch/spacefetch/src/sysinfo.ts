// System info from fastfetch in pipe mode ("Key: value" per line), plus the
// memory fill read straight from /proc, which picks the zone.

export type Entry = { key: string; value: string }

const MODULES = [
  'OS', 'Host', 'Kernel', 'Uptime', 'Packages', 'Shell', 'Display', 'CPU', 'GPU',
  'Memory', 'Swap', 'Disk', 'WM', 'WMTheme', 'Cursor', 'Terminal', 'TerminalFont', 'LocalIp',
]

/** fastfetch's long keys, shortened to fit the panel's key column. */
const SHORT_KEYS: Record<string, string> = {
  'Window Manager': 'WM',
  'WM Theme': 'Theme',
  'Terminal Font': 'Font',
  'Local IP': 'IP',
}

/**
 * fastfetch names the shell by walking the process tree, which would find Bun
 * here and print "Shell: bun". Going through the user's own shell instead makes
 * the module report the real one. The trailing `true` is load-bearing: without
 * it the shell execs fastfetch and Bun is the parent once more.
 */
async function readPipe(): Promise<string> {
  const shell = process.env.SHELL ?? '/bin/sh'
  const child = Bun.spawn([shell, '-c', `fastfetch -c none --pipe -l none -s ${MODULES.join(':')} ; true`], {
    stdout: 'pipe',
    stderr: 'ignore',
  })

  return await new Response(child.stdout).text()
}

/**
 * fastfetch reads the terminal off the process tree and stops at the first
 * non-shell ancestor, which is Bun. `$TERM` names the real one instead; null
 * when it is a generic value (`xterm-256color`) that names no emulator.
 */
function terminalName(): string | null {
  if (process.env.TERM_PROGRAM) return process.env.TERM_PROGRAM

  const known: Record<string, string> = {
    foot: 'foot',
    alacritty: 'alacritty',
    wezterm: 'wezterm',
    kitty: 'kitty',
    'xterm-kitty': 'kitty',
    'xterm-ghostty': 'ghostty',
    'xterm-256color': 'xterm-256color',
  }

  return known[process.env.TERM ?? ''] ?? null
}

export async function readSysinfo(): Promise<Entry[]> {
  const text = await readPipe()
  const terminal = terminalName()

  const entries: Entry[] = text
    .split('\n')
    .map(line => line.match(/^([^:]+):\s(.*)$/))
    .filter(match => match !== null)
    .map(([, rawKey, value]) => {
      // "Display (LU28R55)" → "Display"; the parenthesis is detail the value already carries.
      const key = rawKey!.replace(/\s*\(.*\)$/, '')

      // "[External]" and "- ext4" are fastfetch's footnotes; they only force a wrap.
      const clean = value!.replace(/\s*\[[^\]]*\]/g, '').replace(/\s+-\s+\w+$/, '').trim()

      return { key: SHORT_KEYS[key] ?? key, value: clean }
    })

  return terminal === null ? entries : entries.map(entry => (entry.key === 'Terminal' ? { key: 'Terminal', value: terminal } : entry))
}

/** Used memory as a whole percentage, the same reading fastfetch reports. */
export async function memoryPercent(): Promise<number> {
  const meminfo = await Bun.file('/proc/meminfo').text()
  const read = (name: string) => Number(meminfo.match(new RegExp(`^${name}:\\s+(\\d+)`, 'm'))?.[1] ?? 0)
  const total = read('MemTotal')

  return total > 0 ? Math.round(((total - read('MemAvailable')) / total) * 100) : 0
}
