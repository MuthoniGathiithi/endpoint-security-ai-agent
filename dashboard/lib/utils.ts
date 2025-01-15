import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
 
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date | string | number) {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date))
}

export function formatBytes(bytes: number, decimals = 2) {
  if (bytes === 0) return "0 Bytes"
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i]
}

export function capitalize(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

export function truncate(str: string, length: number) {
  return str.length > length ? str.substring(0, length) + "..." : str
}

export function isMacOS() {
  return typeof navigator !== 'undefined' ? /Mac/.test(navigator.platform) : false
}

export function isWindows() {
  return typeof navigator !== 'undefined' ? /Win/.test(navigator.platform) : false
}

export function isLinux() {
  return typeof navigator !== 'undefined' ? /Linux/.test(navigator.platform) : false
}

export function getOS() {
  if (typeof navigator === 'undefined') return 'unknown'
  if (isMacOS()) return 'macos'
  if (isWindows()) return 'windows'
  if (isLinux()) return 'linux'
  return 'unknown'
}
