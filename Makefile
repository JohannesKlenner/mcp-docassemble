# Makefile für MCP Docassemble Server Docker Operations
# Vereinfacht Build, Test und Deployment

# ============================================================================
# CONFIGURATION
# ============================================================================
IMAGE_NAME := mcp-docassemble-server
VERSION := 1.1.0
REGISTRY := ghcr.io
NAMESPACE := $(shell whoami)
FULL_IMAGE := $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME)

# Default environment
DOCASSEMBLE_URL ?= http://192.168.178.29
DOCASSEMBLE_API_KEY ?= X1IgbwNOk0b0LQ6LS46eSYfj8Ycj4ICU

# ============================================================================
# DEFAULT TARGET
# ============================================================================
.PHONY: help
help: ## Show this help message
	@echo "🐳 MCP Docassemble Server - Docker Commands"
	@echo "============================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================================================
# BUILD COMMANDS
# ============================================================================
.PHONY: build
build: ## Build production Docker image
	@echo "🏗️  Building production image..."
	docker build -t $(IMAGE_NAME):latest -t $(IMAGE_NAME):$(VERSION) .
	@echo "✅ Build completed: $(IMAGE_NAME):$(VERSION)"

.PHONY: build-dev
build-dev: ## Build development Docker image
	@echo "🏗️  Building development image..."
	docker build -f Dockerfile.dev -t $(IMAGE_NAME):dev .
	@echo "✅ Development build completed: $(IMAGE_NAME):dev"

.PHONY: build-all
build-all: build build-dev ## Build all Docker images

# ============================================================================
# RUN COMMANDS
# ============================================================================
.PHONY: run
run: ## Run production container
	@echo "🚀 Starting production container..."
	docker run -d \
		--name mcp-docassemble \
		-p 8080:8080 \
		-e DOCASSEMBLE_URL=$(DOCASSEMBLE_URL) \
		-e DOCASSEMBLE_API_KEY=$(DOCASSEMBLE_API_KEY) \
		$(IMAGE_NAME):latest
	@echo "✅ Container started at http://localhost:8080"

.PHONY: run-dev
run-dev: ## Run development container with hot reload
	@echo "🚀 Starting development container..."
	docker run -d \
		--name mcp-docassemble-dev \
		-p 8081:8080 \
		-v $(PWD)/src:/app/src \
		-v $(PWD)/mcp_docassemble:/app/mcp_docassemble \
		-e DOCASSEMBLE_URL=$(DOCASSEMBLE_URL) \
		-e DOCASSEMBLE_API_KEY=$(DOCASSEMBLE_API_KEY) \
		$(IMAGE_NAME):dev
	@echo "✅ Development container started at http://localhost:8081"

.PHONY: run-interactive
run-interactive: ## Run container interactively for debugging
	@echo "🔧 Starting interactive container..."
	docker run -it --rm \
		-p 8080:8080 \
		-v $(PWD)/src:/app/src \
		-v $(PWD)/mcp_docassemble:/app/mcp_docassemble \
		-e DOCASSEMBLE_URL=$(DOCASSEMBLE_URL) \
		-e DOCASSEMBLE_API_KEY=$(DOCASSEMBLE_API_KEY) \
		$(IMAGE_NAME):dev bash

# ============================================================================
# DOCKER COMPOSE COMMANDS
# ============================================================================
.PHONY: up
up: ## Start full stack with docker-compose
	@echo "🚀 Starting MCP stack..."
	docker-compose up -d
	@echo "✅ Stack started - MCP: http://localhost:8080"

.PHONY: up-dev
up-dev: ## Start development stack
	@echo "🚀 Starting development stack..."
	docker-compose --profile dev up -d
	@echo "✅ Development stack started - MCP: http://localhost:8081"

.PHONY: up-full
up-full: ## Start full stack with monitoring
	@echo "🚀 Starting full monitoring stack..."
	docker-compose --profile monitoring --profile logging up -d
	@echo "✅ Full stack started:"
	@echo "   - MCP Server: http://localhost:8080"
	@echo "   - Grafana: http://localhost:3000"
	@echo "   - Prometheus: http://localhost:9090"
	@echo "   - Kibana: http://localhost:5601"

.PHONY: down
down: ## Stop and remove all containers
	@echo "🛑 Stopping MCP stack..."
	docker-compose down -v
	@echo "✅ Stack stopped and volumes removed"

# ============================================================================
# TESTING & SECURITY
# ============================================================================
.PHONY: test
test: ## Run tests in container
	@echo "🧪 Running tests..."
	docker run --rm \
		-v $(PWD)/tests:/app/tests \
		$(IMAGE_NAME):dev \
		pytest tests/ -v

.PHONY: test-api
test-api: ## Test API endpoints against running server
	@echo "🧪 Testing API endpoints..."
	docker run --rm \
		--network host \
		-e DOCASSEMBLE_URL=$(DOCASSEMBLE_URL) \
		-e DOCASSEMBLE_API_KEY=$(DOCASSEMBLE_API_KEY) \
		$(IMAGE_NAME):dev \
		python test_auth_fixes.py --server-url $(DOCASSEMBLE_URL)

.PHONY: scan
scan: ## Security scan with Trivy
	@echo "🔍 Scanning image for vulnerabilities..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy:latest image $(IMAGE_NAME):latest

.PHONY: scan-detailed
scan-detailed: ## Detailed security scan
	@echo "🔍 Detailed security scan..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy:latest image --severity HIGH,CRITICAL $(IMAGE_NAME):latest

# ============================================================================
# REGISTRY OPERATIONS
# ============================================================================
.PHONY: login
login: ## Login to container registry
	@echo "🔑 Logging in to $(REGISTRY)..."
	echo $(GITHUB_TOKEN) | docker login $(REGISTRY) -u $(GITHUB_USER) --password-stdin

.PHONY: tag
tag: ## Tag image for registry
	@echo "🏷️  Tagging image..."
	docker tag $(IMAGE_NAME):latest $(FULL_IMAGE):latest
	docker tag $(IMAGE_NAME):latest $(FULL_IMAGE):$(VERSION)

.PHONY: push
push: tag ## Push image to registry
	@echo "📤 Pushing to registry..."
	docker push $(FULL_IMAGE):latest
	docker push $(FULL_IMAGE):$(VERSION)
	@echo "✅ Pushed to: $(FULL_IMAGE):$(VERSION)"

.PHONY: pull
pull: ## Pull image from registry
	@echo "📥 Pulling from registry..."
	docker pull $(FULL_IMAGE):latest

# ============================================================================
# MAINTENANCE COMMANDS
# ============================================================================
.PHONY: logs
logs: ## Show container logs
	docker logs -f mcp-docassemble

.PHONY: logs-dev
logs-dev: ## Show development container logs
	docker logs -f mcp-docassemble-dev

.PHONY: shell
shell: ## Open shell in running container
	docker exec -it mcp-docassemble bash

.PHONY: stats
stats: ## Show container stats
	docker stats mcp-docassemble

.PHONY: health
health: ## Check container health
	@echo "🏥 Health check..."
	curl -f http://localhost:8080/health || echo "❌ Health check failed"

# ============================================================================
# CLEANUP COMMANDS
# ============================================================================
.PHONY: stop
stop: ## Stop running containers
	@echo "🛑 Stopping containers..."
	-docker stop mcp-docassemble mcp-docassemble-dev
	@echo "✅ Containers stopped"

.PHONY: clean
clean: stop ## Stop and remove containers
	@echo "🧹 Cleaning up containers..."
	-docker rm mcp-docassemble mcp-docassemble-dev
	@echo "✅ Containers removed"

.PHONY: clean-images
clean-images: ## Remove built images
	@echo "🧹 Cleaning up images..."
	-docker rmi $(IMAGE_NAME):latest $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):dev
	@echo "✅ Images removed"

.PHONY: clean-all
clean-all: clean clean-images ## Complete cleanup
	@echo "🧹 Complete cleanup..."
	docker system prune -f
	@echo "✅ Complete cleanup done"

# ============================================================================
# QUICK COMMANDS
# ============================================================================
.PHONY: quick-test
quick-test: build test ## Quick build and test
	@echo "✅ Quick test completed"

.PHONY: quick-deploy
quick-deploy: build scan push ## Quick build, scan and deploy
	@echo "✅ Quick deploy completed"

.PHONY: dev-start
dev-start: build-dev run-dev ## Start development environment
	@echo "✅ Development environment ready at http://localhost:8081"

.PHONY: prod-start
prod-start: build run ## Start production environment
	@echo "✅ Production environment ready at http://localhost:8080"

# ============================================================================
# INFORMATION
# ============================================================================
.PHONY: info
info: ## Show build information
	@echo "📊 MCP Docassemble Server Build Info"
	@echo "===================================="
	@echo "Image Name: $(IMAGE_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Registry: $(FULL_IMAGE)"
	@echo "Docassemble URL: $(DOCASSEMBLE_URL)"
	@echo ""
	@echo "Available images:"
	@docker images $(IMAGE_NAME) --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"
