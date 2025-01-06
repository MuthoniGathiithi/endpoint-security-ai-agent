# Deploying to Render

This guide will help you deploy the Endpoint Security AI Agent to Render.

## Prerequisites

- Render account (https://render.com)
- GitHub account with this repository
- (Optional) OpenAI API key for AI analyst features

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select this repository
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables**
   - Backend service:
     - `SECRET_KEY`: Generate a strong random key
     - `OPENAI_API_KEY`: (Optional) Your OpenAI API key
   - Frontend service:
     - Auto-configured to connect to backend

4. **Deploy**
   - Click "Create Blueprint"
   - Render will automatically build and deploy both services

### Option 2: Manual Deployment

#### Deploy Backend

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Runtime**: Python 3.10
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     DEBUG=false
     DATABASE_URL=sqlite:///./data/edr.db
     SECRET_KEY=<generate-strong-random-key>
     OPENAI_API_KEY=<your-openai-key>
     ```

#### Deploy Frontend

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Runtime**: Node 18
   - **Build Command**: `cd dashboard && npm install && npm run build`
   - **Start Command**: `cd dashboard && npm start`
   - **Environment Variables**:
     ```
     NEXT_PUBLIC_API_URL=<backend-url>/api/v1
     NEXT_PUBLIC_WS_URL=<backend-url-with-ws>/ws
     NODE_ENV=production
     ```

## Environment Variables

### Backend

| Variable | Description | Required |
|----------|-------------|----------|
| `DEBUG` | Enable debug mode | No (default: false) |
| `DATABASE_URL` | Database connection string | No (default: SQLite) |
| `SECRET_KEY` | JWT secret key | Yes (generate strong key) |
| `OPENAI_API_KEY` | OpenAI API key for AI analyst | No |
| `LOG_LEVEL` | Logging level | No (default: INFO) |

### Frontend

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |
| `NEXT_PUBLIC_WS_URL` | WebSocket URL | Yes |
| `NODE_ENV` | Node environment | No (default: production) |

## Accessing Your Deployment

Once deployed:

- **Dashboard**: `https://<your-frontend-service>.onrender.com`
- **API**: `https://<your-backend-service>.onrender.com/api/v1`
- **API Docs**: `https://<your-backend-service>.onrender.com/api/docs`

## Database

By default, the application uses SQLite with file-based storage at `./data/edr.db`.

For production, consider:
- Using PostgreSQL on Render
- Updating `DATABASE_URL` to PostgreSQL connection string

## Limitations on Free Tier

- Services spin down after 15 minutes of inactivity
- Limited to 0.5 GB RAM
- 100 GB bandwidth/month

For production use, upgrade to paid plans.

## Troubleshooting

### Services Won't Start

Check logs in Render dashboard:
1. Go to your service
2. Click "Logs"
3. Look for error messages

### Frontend Can't Connect to Backend

- Verify `NEXT_PUBLIC_API_URL` is correct
- Ensure backend service is running
- Check CORS settings in backend

### Database Errors

- Ensure `DATABASE_URL` is correct
- For SQLite, ensure `/data` directory exists
- Check file permissions

## Scaling

To improve performance:
1. Upgrade to paid Render plan
2. Increase RAM allocation
3. Use PostgreSQL instead of SQLite
4. Enable caching

## Support

For issues:
1. Check Render documentation: https://render.com/docs
2. Review application logs
3. Open an issue on GitHub

## Security Notes

- Always use strong `SECRET_KEY` in production
- Rotate API keys regularly
- Use HTTPS (automatic on Render)
- Enable authentication for sensitive endpoints
- Keep dependencies updated

## Next Steps

After deployment:
1. Access your dashboard
2. Run attack simulator to test detection
3. Configure alert thresholds
4. Set up playbooks for automated response
5. Integrate with your security team's tools
