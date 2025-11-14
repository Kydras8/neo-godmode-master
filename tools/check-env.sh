#!/usr/bin/env bash
# Environment validation script for Neo Godmode
set -euo pipefail

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Neo Godmode — Environment Configuration Check            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BAREMETAL_PATH="kits/neo-godmode-baremetal-kit/neo-godmode"
ENV_FILE="$BAREMETAL_PATH/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}❌ .env file not found at $ENV_FILE${NC}"
    echo "  Run: cp $BAREMETAL_PATH/.env.example $ENV_FILE"
    exit 1
fi

echo "Checking $ENV_FILE..."
echo ""

ERRORS=0
WARNINGS=0

# Required variables
check_required() {
    local var_name=$1
    local friendly_name=$2
    
    if grep -q "^${var_name}=" "$ENV_FILE"; then
        local value=$(grep "^${var_name}=" "$ENV_FILE" | cut -d'=' -f2-)
        if [ -z "$value" ] || [ "$value" = "your_key_here" ] || [ "$value" = "change-me" ]; then
            echo -e "${RED}✗ ${friendly_name} (${var_name}) is not set${NC}"
            ((ERRORS++))
        else
            echo -e "${GREEN}✓ ${friendly_name} (${var_name})${NC}"
        fi
    else
        echo -e "${RED}✗ ${friendly_name} (${var_name}) is missing${NC}"
        ((ERRORS++))
    fi
}

# Optional but recommended variables
check_optional() {
    local var_name=$1
    local friendly_name=$2
    
    if grep -q "^${var_name}=" "$ENV_FILE"; then
        local value=$(grep "^${var_name}=" "$ENV_FILE" | cut -d'=' -f2-)
        if [ -z "$value" ] || [ "$value" = "your_key_here" ] || [ "$value" = "change-me" ]; then
            echo -e "${YELLOW}⚠ ${friendly_name} (${var_name}) uses default value${NC}"
            ((WARNINGS++))
        else
            echo -e "${GREEN}✓ ${friendly_name} (${var_name})${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ ${friendly_name} (${var_name}) is not set${NC}"
        ((WARNINGS++))
    fi
}

# Check default values that should be changed
check_security() {
    local var_name=$1
    local friendly_name=$2
    local default_pattern=$3
    
    if grep -q "^${var_name}=" "$ENV_FILE"; then
        local value=$(grep "^${var_name}=" "$ENV_FILE" | cut -d'=' -f2-)
        if echo "$value" | grep -q "$default_pattern"; then
            echo -e "${YELLOW}⚠ ${friendly_name} (${var_name}) uses insecure default${NC}"
            ((WARNINGS++))
        else
            echo -e "${GREEN}✓ ${friendly_name} (${var_name})${NC}"
        fi
    fi
}

echo "Required Configuration:"
check_required "OPENAI_API_KEY" "OpenAI API Key"
check_required "OPENAI_MODEL" "OpenAI Model"

echo ""
echo "Optional Services:"
check_optional "SERPAPI_API_KEY" "SerpAPI Key"

echo ""
echo "Security Configuration:"
check_security "ACTIONS_API_KEY" "Actions API Key" "change-me"
check_security "JWT_SECRET" "JWT Secret" "hyygGquc7L2hN4ZXZiT_mgQKw6R3fmpgZCqzDK_OPRs"
check_optional "JWT_ALG" "JWT Algorithm"
check_optional "JWT_ISS" "JWT Issuer"
check_optional "JWT_AUD" "JWT Audience"

echo ""
echo "Production Settings:"
check_optional "DOMAIN" "Domain"
check_optional "TRAEFIK_EMAIL" "Traefik Email"

echo ""
echo "Database Configuration:"
check_optional "POSTGRES_USER" "Postgres User"
check_security "POSTGRES_PASSWORD" "Postgres Password" "change-me"
check_optional "POSTGRES_DB" "Postgres Database"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Summary:"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ ${WARNINGS} warning(s) found${NC}"
    echo "  Your configuration will work but consider updating warned values"
    exit 0
else
    echo -e "${RED}✗ ${ERRORS} error(s) found${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ ${WARNINGS} warning(s) found${NC}"
    fi
    echo ""
    echo "Please fix the errors before running Neo Godmode"
    exit 1
fi
