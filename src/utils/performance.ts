export function debounce<TArguments extends readonly unknown[]>(
  callback: (...arguments_: TArguments) => void,
  delayMs: number
): (...arguments_: TArguments) => void {
  let timer: ReturnType<typeof setTimeout> | undefined;
  return (...arguments_: TArguments) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => callback(...arguments_), delayMs);
  };
}

export function createAbortableRequest(): {
  readonly signal: AbortSignal;
  readonly cancel: () => void;
} {
  const controller = new AbortController();
  return { signal: controller.signal, cancel: () => controller.abort() };
}
