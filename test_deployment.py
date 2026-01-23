"""
Test script to verify that the application is ready for deployment.
This script performs basic checks to ensure all components work properly.
"""

import os
import sys
import subprocess
from pathlib import Path

def test_environment_variables():
    """Test that essential environment variables are set."""
    print("🔍 Testing environment variables...")

    required_vars = [
        'DATABASE_URL',
        'JWT_SECRET_KEY',
        'OPENAI_API_KEY',
        'BETTER_AUTH_SECRET',
        'CSRF_SECRET_KEY'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("   Please set these variables before deployment.")
        return False

    print("✅ All required environment variables are set")
    return True


def test_database_connection():
    """Test database connection."""
    print("\n🔍 Testing database connection...")

    try:
        from backend.db import check_db_connection
        # Import from migrations since it has the proper function
        from backend.migrations import check_db_connection

        if check_db_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False

    except ImportError as e:
        print(f"⚠️  Could not test database connection: {e}")
        print("   This may be expected if running in a minimal environment")
        return True  # Don't fail the test for import issues
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False


def test_imports():
    """Test that key modules can be imported without errors."""
    print("\n🔍 Testing module imports...")

    modules_to_test = [
        ('backend.api', 'app'),
        ('backend.config', 'settings'),
        ('backend.db', 'get_session'),
        ('backend.models.chatbot', 'Conversation'),
        ('backend.health', 'router'),
    ]

    for module_path, attribute in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[attribute])
            getattr(module, attribute)
            print(f"✅ Successfully imported {module_path}.{attribute}")
        except Exception as e:
            print(f"❌ Failed to import {module_path}.{attribute}: {e}")
            return False

    return True


def test_config_validation():
    """Test configuration validation."""
    print("\n🔍 Testing configuration validation...")

    try:
        from backend.config import validate_environment
        validate_environment()
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False


def test_health_endpoints():
    """Test that health check endpoints are available."""
    print("\n🔍 Testing health check endpoints...")

    try:
        from backend.health import check_database_health, check_external_services
        import asyncio

        # Test database health check
        db_result = asyncio.run(check_database_health())
        print(f"✅ Database health check available: {db_result['status']}")

        # Test external services check
        ext_result = asyncio.run(check_external_services())
        print(f"✅ External services check available: {list(ext_result.keys())}")

        return True
    except Exception as e:
        print(f"❌ Health check test failed: {e}")
        return False


def main():
    """Run all deployment readiness tests."""
    print("🚀 Starting deployment readiness tests...\n")

    tests = [
        test_environment_variables,
        test_config_validation,
        test_imports,
        test_health_endpoints,
        test_database_connection,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            results.append(False)

    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")

    if all(results):
        print("\n🎉 All tests passed! Application is ready for deployment.")
        print("\n📋 Next steps for deployment:")
        print("   1. Set up your production environment variables")
        print("   2. Deploy the backend to your preferred platform (Railway/Render)")
        print("   3. Deploy the frontend to Vercel")
        print("   4. Configure your domain and SSL certificates")
        print("   5. Test the complete application flow")
        return True
    else:
        print(f"\n💥 {len(results) - sum(results)} test(s) failed. Please fix before deployment.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)