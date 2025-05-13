# API Examples

Here are some example curl requests for the main API endpoints. Replace `your-auth-token` with the actual token you receive after authentication.

## Authentication

Get authentication token:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

## Customer Profile

Create a new customer profile:
```bash
curl -X POST http://localhost:8000/api/accounts/customers/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
      "username": "customer1",
      "email": "customer1@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "customer_id": "CUST001",
    "phone_number": "+1234567890",
    "address": "123 Main St, City, Country"
  }'
```

Get customer profile:
```bash
curl -X GET http://localhost:8000/api/accounts/customers/my_profile/ \
  -H "Authorization: Token your-auth-token"
```

## Service Requests

Create a service type:
```bash
curl -X POST http://localhost:8000/api/services/types/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gas Leak Repair",
    "description": "Emergency repair service for gas leaks",
    "estimated_time": 2
  }'
```

Create a service request:
```bash
curl -X POST http://localhost:8000/api/services/requests/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "service_type_id": 1,
    "description": "Detected gas leak in kitchen",
    "priority": "HIGH"
  }'
```

Get service request details:
```bash
curl -X GET http://localhost:8000/api/services/requests/1/ \
  -H "Authorization: Token your-auth-token"
```

Update service request status:
```bash
curl -X POST http://localhost:8000/api/services/requests/1/update_status/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{"status": "IN_PROGRESS"}'
```

Add comment to service request:
```bash
curl -X POST http://localhost:8000/api/services/requests/1/comments/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": "Technician will arrive within 1 hour"
  }'
```

## Support Tickets

Create support ticket:
```bash
curl -X POST http://localhost:8000/api/support/tickets/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "service_request_id": 1,
    "description": "Customer reported strong gas smell",
    "priority": "HIGH"
  }'
```

Resolve support ticket:
```bash
curl -X POST http://localhost:8000/api/support/tickets/1/resolve/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "resolution_notes": "Gas leak fixed and safety check completed"
  }'
```

Record customer interaction:
```bash
curl -X POST http://localhost:8000/api/support/interactions/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "support_ticket_id": 1,
    "interaction_type": "CALL",
    "notes": "Discussed ETA with customer",
    "duration": 5
  }'
```

Get interaction statistics:
```bash
curl -X GET http://localhost:8000/api/support/interactions/interaction_stats/ \
  -H "Authorization: Token your-auth-token"
```

## File Upload Example

Upload attachment with service request:
```bash
curl -X POST http://localhost:8000/api/services/requests/ \
  -H "Authorization: Token your-auth-token" \
  -F "service_type_id=1" \
  -F "description=Gas leak with visible damage" \
  -F "priority=HIGH" \
  -F "attachment=@/path/to/photo.jpg"
```

Note: All these examples assume your server is running locally on port 8000. Adjust the URL accordingly if your server is hosted elsewhere.
