/**
 * Utility to conditionally join class names together.
 * Accepts strings, undefined, null, false, and objects with boolean values.
 *
 * Usage:
 *   classNames("foo", "bar")                    // "foo bar"
 *   classNames("foo", false && "bar")            // "foo"
 *   classNames("foo", { bar: true, baz: false }) // "foo bar"
 *   classNames("foo", undefined, "bar")          // "foo bar"
 */
type ClassValue =
  | string
  | number
  | boolean
  | undefined
  | null
  | Record<string, boolean | undefined | null>;

export function classNames(...args: ClassValue[]): string {
  const classes: string[] = [];

  for (const arg of args) {
    if (!arg) continue;

    if (typeof arg === "string" || typeof arg === "number") {
      classes.push(String(arg));
    } else if (typeof arg === "object") {
      for (const [key, value] of Object.entries(arg)) {
        if (value) {
          classes.push(key);
        }
      }
    }
  }

  return classes.join(" ");
}
