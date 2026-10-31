import axios from "axios";

// Future REST integration boundary. The current UI intentionally uses local mock state.
export const api = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL || "/api" });
