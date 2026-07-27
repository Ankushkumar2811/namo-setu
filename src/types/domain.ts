export type UserRole = "user" | "temple_admin" | "partner" | "guide" | "hotel" | "super_admin";
export type BookingStatus = "draft" | "pending_payment" | "confirmed" | "in_progress" | "completed" | "cancelled";
export type CrowdLevel = "low" | "moderate" | "high" | "critical";

export interface GeoPoint {
  readonly latitude: number;
  readonly longitude: number;
}

export interface TempleSummary {
  readonly id: string;
  readonly slug: string;
  readonly name: string;
  readonly city: string;
  readonly state: string;
  readonly category: string;
  readonly rating: number;
  readonly crowdLevel: CrowdLevel;
  readonly queueMinutes: number;
  readonly location: GeoPoint;
}

export interface JourneyPreferences {
  readonly destination: string;
  readonly travellers: number;
  readonly durationDays: number;
  readonly budgetInr?: number;
  readonly seniorFriendly: boolean;
  readonly accessibilityNeeds: readonly string[];
}

export interface Booking {
  readonly id: string;
  readonly userId: string;
  readonly productType: "hotel" | "dharamshala" | "cab" | "guide" | "puja" | "donation";
  readonly status: BookingStatus;
  readonly amountInr: number;
  readonly createdAt: string;
}
