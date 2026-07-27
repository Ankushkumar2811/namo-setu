export type RealtimeEvent =
  | { readonly type: "queue.updated"; readonly templeId: string; readonly minutes: number }
  | { readonly type: "booking.updated"; readonly bookingId: string; readonly status: string }
  | { readonly type: "emergency.alert"; readonly title: string; readonly message: string }
  | { readonly type: "weather.alert"; readonly destinationId: string; readonly message: string };

export class RealtimeClient {
  private source: EventSource | undefined;
  private reconnectAttempt = 0;

  connect(url: string, onEvent: (event: RealtimeEvent) => void): void {
    this.disconnect();
    this.source = new EventSource(url, { withCredentials: true });
    this.source.onmessage = message => {
      const event = JSON.parse(message.data) as RealtimeEvent;
      onEvent(event);
    };
    this.source.onopen = () => { this.reconnectAttempt = 0; };
    this.source.onerror = () => {
      this.disconnect();
      const delay = Math.min(30_000, 1_000 * 2 ** this.reconnectAttempt++);
      window.setTimeout(() => this.connect(url, onEvent), delay);
    };
  }

  disconnect(): void {
    this.source?.close();
    this.source = undefined;
  }
}
