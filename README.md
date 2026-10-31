# Subscription_Management_System

## MongoDB connection

1. Copy `.env.example` to `.env`.
2. Replace the placeholder values with a newly rotated Atlas database user and the
   current connection string from Atlas.
3. Add your current public IP address to Atlas **Network Access**.
4. Run `python MongoDB\mongoDB_connection.py`.

The connection check uses PyMongo's MongoDB handshake. Do not test an Atlas
connection with a raw TLS socket, because that does not perform the MongoDB
protocol handshake.