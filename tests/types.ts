export type User = {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: Date;
  updatedAt: Date;
};

export type AuthToken = {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
};

export type AuthPayload = {
  userId: string;
  role: 'admin' | 'user' | 'guest';
};

export type LoginRequest = {
  email: string;
  password: string;
};

export type RegisterRequest = {
  email: string;
  name: string;
  password: string;
  role?: 'admin' | 'user' | 'guest';
};

export type RefreshTokenRequest = {
  refreshToken: string;
};

export type ErrorResponse = {
  error: string;
  message: string;
  statusCode: number;
};

export type PaginationParams = {
  page: number;
  limit: number;
};

export type PaginatedResponse<T> = {
  data: T[];
  total: number;
  page: number;
  limit: number;
};