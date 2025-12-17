// types.ts

export interface User {
  id: string;
  username: string;
  email: string;
  password: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface AuthToken {
  token: string;
  expiresAt: Date;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface ErrorResponse {
  code: number;
  message: string;
  details: string[];
}

export enum ErrorCode {
  InvalidCredentials = 401,
  UserAlreadyExists = 409,
  InternalServerError = 500,
}

export interface AuthGatewayOptions {
  secretKey: string;
  tokenExpirationTime: number;
}