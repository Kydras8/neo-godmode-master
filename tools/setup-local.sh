#!/usr/bin/env bash
# Local development setup script for Neo Godmode
set -euo pipefail

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Neo Godmode — Local Development Setup                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "kits" ]; then
    echo -e "${RED}❌ Error: This script must be run from the neo-godmode-master root directory.${NC}"
    exit 1
fi

echo "→ Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "  Please install Python 3.11 or later"
    exit 1
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python ${PYTHON_VERSION}${NC}"
fi

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    echo -e "${GREEN}✓ Docker ${DOCKER_VERSION}${NC}"
else
    echo -e "${YELLOW}⚠ Docker not found (optional for local dev)${NC}"
fi

# Check git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo -e "${GREEN}✓ Git ${GIT_VERSION}${NC}"
else
    echo -e "${RED}❌ Git is not installed${NC}"
    exit 1
fi

echo ""
echo "→ Setting up environment..."

# Navigate to baremetal kit (canonical location)
BAREMETAL_PATH="kits/neo-godmode-baremetal-kit/neo-godmode"

if [ ! -d "$BAREMETAL_PATH" ]; then
    echo -e "${RED}❌ Baremetal kit not found at $BAREMETAL_PATH${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f "$BAREMETAL_PATH/.env" ]; then
    echo -e "${YELLOW}→ Creating .env file from template...${NC}"
    cp "$BAREMETAL_PATH/.env.example" "$BAREMETAL_PATH/.env"
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo -e "${YELLOW}⚠ Please edit $BAREMETAL_PATH/.env and add your API keys${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Create necessary directories
echo "→ Creating directories..."
mkdir -p "$BAREMETAL_PATH/data"
mkdir -p "$BAREMETAL_PATH/deliverables"
mkdir -p "$BAREMETAL_PATH/logs"
echo -e "${GREEN}✓ Directories created${NC}"

# Install Python dependencies
echo ""
echo "→ Installing Python dependencies..."

for component in actions api orchestrator worker; do
    REQ_FILE="$BAREMETAL_PATH/$component/requirements.txt"
    if [ -f "$REQ_FILE" ]; then
        echo -e "${YELLOW}  Installing $component dependencies...${NC}"
        python3 -m pip install -q -r "$REQ_FILE" || {
            echo -e "${YELLOW}  ⚠ Some dependencies failed to install for $component${NC}"
        }
    fi
done

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check environment file
echo ""
echo "→ Validating environment configuration..."

if grep -q "sk-..." "$BAREMETAL_PATH/.env" 2>/dev/null; then
    echo -e "${YELLOW}⚠ OPENAI_API_KEY appears to be the example value${NC}"
    echo "  Please update it in $BAREMETAL_PATH/.env"
fi

if grep -q "your_serpapi_key" "$BAREMETAL_PATH/.env" 2>/dev/null; then
    echo -e "${YELLOW}⚠ SERPAPI_API_KEY appears to be the example value${NC}"
    echo "  Please update it in $BAREMETAL_PATH/.env"
fi

if grep -q "change-me" "$BAREMETAL_PATH/.env" 2>/dev/null; then
    echo -e "${YELLOW}⚠ Some secrets still have default values${NC}"
    echo "  Please review and update $BAREMETAL_PATH/.env"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✓ Local Development Setup Complete!                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your API keys in:"
echo "   $BAREMETAL_PATH/.env"
echo ""
echo "2. Run with Docker:"
echo "   cd $BAREMETAL_PATH/infra"
echo "   docker compose up --build"
echo ""
echo "3. Or run individual components without Docker:"
echo "   # Actions API:"
echo "   python3 $BAREMETAL_PATH/actions/app.py"
echo ""
echo "   # API Skeleton:"
echo "   python3 $BAREMETAL_PATH/api/neo_openai_skeleton.py"
echo ""
echo "   # Orchestrator:"
echo "   python3 $BAREMETAL_PATH/orchestrator/neo_orchestrator_real.py"
echo ""
echo "For more information, see docs/readme.md"
echo ""
