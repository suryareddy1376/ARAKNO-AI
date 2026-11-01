# ARAKNO-AI Troubleshooting

## Common Issues

### Backend won't start

**Symptom**: `ModuleNotFoundError` when starting backend

**Solution**:
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Symptom**: Port 8000 already in use

**Solution**:
```powershell
# Find and stop the process using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
Stop-Process -Id <PID>
```

### Frontend won't start

**Symptom**: `npm ERR!` during startup

**Solution**:
```powershell
cd frontend
Remove-Item -Recurse node_modules -ErrorAction SilentlyContinue
npm install
npm run dev
```

### Database errors

**Symptom**: `OperationalError: database is locked`

**Solution**: Only one backend instance should access the database. Stop duplicate processes:
```powershell
.\scripts\stop-all.ps1
.\scripts\run-all.ps1
```

**Symptom**: Database corruption

**Solution**: Delete and recreate:
```powershell
Remove-Item data\database\arakno.db
# Database will be recreated on next backend start
```

### API connectivity issues

**Symptom**: PubMed searches return errors

**Possible causes**:
1. No internet connection
2. NCBI rate limiting (set `NCBI_EMAIL` in `.env`)
3. NCBI service temporarily unavailable

**Symptom**: AlphaFold returns no results

**Possible causes**:
1. Invalid UniProt accession
2. No prediction available for that protein
3. AlphaFold API temporarily unavailable

### LLM issues

**Symptom**: "LLM not configured" messages

**Expected behavior**: LLM is disabled by default. Set `LLM_PROVIDER` in `.env` if you want AI features.

**Symptom**: "Paid request blocked"

**Expected behavior**: Set `ALLOW_PAID_REQUESTS=true` in `.env` if you want to use paid models.

### Memory issues

**Symptom**: Application crashes or becomes slow

**Solutions**:
1. Close unnecessary browser tabs
2. Limit concurrent API searches
3. Clear cache: `Remove-Item data\cache\* -Recurse`
4. Reduce `PUBMED_MAX_RESULTS` in `.env`

### Python version compatibility

**Symptom**: Package installation fails on Python 3.13

**Solution**: Some packages may not support Python 3.13 yet. Install Python 3.12:
```powershell
# Download from python.org and install alongside 3.13
py -3.12 -m venv backend\venv
```

## Health Check

Run the health check script:
```powershell
python scripts\health-check.py
```

## Getting Help

1. Check the API docs: http://127.0.0.1:8000/docs
2. Review backend logs in the terminal
3. Check browser developer console for frontend errors
