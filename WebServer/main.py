from fastapi import FastAPI
from resources import transaction
from sqlalchemy import text

app = FastAPI(title="LangScribe API Gateway")


def test_with_transaction():
    """Test using your transaction context manager"""
    try:
        with transaction() as session:
            result = session.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"✓ Transaction test successful! Result: {value}")
            return True
    except Exception as e:
        print(f"✗ Transaction test failed: {e}")
        return False

@app.get("/health")
async def health() -> dict[str, str]:
    
    test_with_transaction()
    
    return {"status": "ok", "service": "api-gateway"}
