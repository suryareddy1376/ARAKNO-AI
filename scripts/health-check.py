"""ARAKNO-AI Health Check Script"""
import sys
import json
import time

def check_health():
    """Check the health of ARAKNO-AI services."""
    try:
        import urllib.request
        import urllib.error
    except ImportError:
        print("ERROR: urllib not available")
        sys.exit(1)

    results = {}

    # Check backend
    print("\nARAKNO-AI Health Check")
    print("=" * 40)

    # Backend health
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/health")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            results["backend"] = {"status": "healthy", "data": data}
            print(f"  Backend:  HEALTHY")
    except urllib.error.URLError:
        results["backend"] = {"status": "unreachable"}
        print(f"  Backend:  UNREACHABLE")
    except Exception as e:
        results["backend"] = {"status": "error", "error": str(e)}
        print(f"  Backend:  ERROR - {e}")

    # System status
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/system/status")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"  Database: {'OK' if data.get('database_connected') else 'ERROR'}")
            print(f"  Storage:  {data.get('data_directory', 'unknown')}")
    except Exception:
        pass

    # Frontend
    try:
        req = urllib.request.Request("http://localhost:5173")
        with urllib.request.urlopen(req, timeout=10) as resp:
            results["frontend"] = {"status": "healthy"}
            print(f"  Frontend: HEALTHY")
    except urllib.error.URLError:
        results["frontend"] = {"status": "unreachable"}
        print(f"  Frontend: UNREACHABLE")
    except Exception as e:
        results["frontend"] = {"status": "error", "error": str(e)}
        print(f"  Frontend: ERROR - {e}")

    print("=" * 40)

    all_healthy = all(r.get("status") == "healthy" for r in results.values())
    if all_healthy:
        print("All services healthy.\n")
    else:
        print("Some services have issues.\n")

    return 0 if all_healthy else 1


if __name__ == "__main__":
    sys.exit(check_health())
