export interface ApiErrorPayload {
  readonly code: string;
  readonly message: string;
  readonly requestId?: string;
}

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly payload?: ApiErrorPayload
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export interface ApiClientOptions {
  readonly baseUrl: string;
  readonly getAccessToken?: () => Promise<string | undefined>;
}

export class ApiClient {
  constructor(private readonly options: ApiClientOptions) {}

  async request<TResponse>(path: string, init: RequestInit = {}): Promise<TResponse> {
    const token = await this.options.getAccessToken?.();
    const response = await fetch(`${this.options.baseUrl}${path}`, {
      ...init,
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        ...(token ? { "Authorization": `Bearer ${token}` } : {}),
        ...init.headers
      }
    });
    if (!response.ok) {
      const payload = await response.json().catch(() => undefined) as ApiErrorPayload | undefined;
      throw new ApiError(payload?.message ?? "Request failed", response.status, payload);
    }
    if (response.status === 204) return undefined as TResponse;
    return response.json() as Promise<TResponse>;
  }
}
