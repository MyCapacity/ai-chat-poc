const env: string = process.env.NODE_ENV;
export const apiServer = `http://${env === "production" ? "advanced-analytics-backend" : "localhost"}:8081`